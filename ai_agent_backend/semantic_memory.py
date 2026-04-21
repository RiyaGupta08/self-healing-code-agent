"""
Semantic Memory Module
Stores error-fix patterns and retrieves similar past errors using FAISS.
Improves fix ranking through learned patterns.
"""

import json
import logging
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

try:
    import faiss
except ImportError:
    faiss = None

from error_detector import ErrorInfo
from planning_module import FixStrategy

try:
    from config_settings import (
        FAISS_INDEX_PATH, EMBEDDING_DIMENSION, TOP_K_MEMORIES,
        MEMORY_DB_PATH, MAX_MEMORY_SIZE
    )
except ImportError:
    FAISS_INDEX_PATH = "models/faiss_index.bin"
    EMBEDDING_DIMENSION = 1000
    TOP_K_MEMORIES = 5
    MEMORY_DB_PATH = "data/memory_store.json"
    MAX_MEMORY_SIZE = 10000


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class MemoryEntry:
    """Stored error-fix memory"""
    error_type: str              # Type of error
    error_message: str           # Error message
    code_snippet: str            # Code context
    fix_applied: Dict[str, Any] # Fix that was applied
    success: bool                # Did fix work?
    timestamp: str               # When stored
    fix_time_seconds: float      # How long to fix
    attempts: int                # Number of attempts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class SimilarMemory:
    """Similar past error retrieved from memory"""
    entry: MemoryEntry
    similarity_score: float      # [0, 1] - higher is more similar
    fix_worked: bool             # Whether the fix worked
    success_rate: float          # Historical success rate
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "entry": self.entry.to_dict(),
            "similarity_score": round(float(self.similarity_score), 4),
            "fix_worked": self.fix_worked,
            "success_rate": round(float(self.success_rate), 4)
        }


# ============================================================================
# SEMANTIC MEMORY MODULE
# ============================================================================

class SemanticMemory:
    """
    Manages error-fix patterns using FAISS for similarity search.
    
    Architecture:
    - Embeddings: Convert error text to vectors (TF-IDF)
    - FAISS Index: Fast similarity search on embeddings
    - JSON Store: Metadata and full entry storage
    - Learning: Track success rates for feedback
    
    Key Features:
    - Retrieve top-K similar past errors
    - Use patterns to improve fix ranking
    - Learn from successes and failures
    - Scalable to thousands of patterns
    """
    
    def __init__(self, 
                 embedding_dim: int = EMBEDDING_DIMENSION,
                 top_k: int = TOP_K_MEMORIES,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize semantic memory.
        
        Args:
            embedding_dim: Dimension of embeddings (TF-IDF features)
            top_k: Number of similar memories to retrieve
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.embedding_dim = embedding_dim
        self.top_k = top_k
        
        # FAISS index for similarity search
        self.faiss_index: Optional[faiss.Index] = None
        
        # In-memory storage (can be persisted to JSON)
        self.memory_entries: List[MemoryEntry] = []
        self.embeddings: Optional[np.ndarray] = None
        
        # Statistics
        self.success_rates: Dict[str, float] = {}  # fix_type -> success_rate
        self.fix_statistics: Dict[str, Dict[str, Any]] = {}  # fix_type -> stats
        
        self.logger.info("SemanticMemory initialized")
    
    def store_error_fix(self,
                       error_type: str,
                       error_message: str,
                       code_snippet: str,
                       fix: FixStrategy,
                       success: bool,
                       fix_time: float,
                       attempts: int) -> None:
        """
        Store an error-fix pattern in memory.
        
        Args:
            error_type: Type of error
            error_message: Error message
            code_snippet: Code context
            fix: Fix that was applied
            success: Whether fix worked
            fix_time: Time to fix in seconds
            attempts: Number of attempts
        """
        # Create memory entry
        entry = MemoryEntry(
            error_type=error_type,
            error_message=error_message,
            code_snippet=code_snippet,
            fix_applied=fix.to_dict(),
            success=success,
            timestamp=datetime.now().isoformat(),
            fix_time_seconds=fix_time,
            attempts=attempts
        )
        
        # Store in memory
        self.memory_entries.append(entry)
        
        # Update statistics
        self._update_statistics(fix.fix_type.value, success, fix_time)
        
        # Rebuild FAISS index if needed
        if len(self.memory_entries) % 10 == 0:
            self._rebuild_faiss_index()
        
        self.logger.info(
            f"Stored error-fix pattern: {error_type} → "
            f"{fix.fix_type.value} (success: {success})"
        )
    
    def retrieve_similar_errors(self,
                               error_text: str,
                               embeddings_vectorizer: Optional[Any] = None) -> List[SimilarMemory]:
        """
        Retrieve top-K similar past errors using FAISS.
        
        Args:
            error_text: Current error description
            embeddings_vectorizer: TF-IDF vectorizer to convert text to embeddings
            
        Returns:
            List of SimilarMemory objects with similarity scores
        """
        if not self.memory_entries or self.faiss_index is None:
            self.logger.debug("No memories to retrieve")
            return []
        
        if embeddings_vectorizer is None:
            self.logger.warning("No vectorizer provided for similarity search")
            return []
        
        try:
            # Vectorize current error
            query_vector = embeddings_vectorizer.transform([error_text]).toarray()
            query_vector = query_vector.astype('float32')
            
            # Search FAISS index
            distances, indices = self.faiss_index.search(query_vector, self.top_k)
            
            # Convert distances to similarity scores
            # FAISS returns L2 distances; convert to similarity [0, 1]
            similarities = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx < len(self.memory_entries):
                    # Convert L2 distance to similarity
                    similarity = 1.0 / (1.0 + distance)
                    entry = self.memory_entries[idx]
                    success_rate = self.success_rates.get(
                        entry.fix_applied['fix_type'], 0.5
                    )
                    
                    similar = SimilarMemory(
                        entry=entry,
                        similarity_score=similarity,
                        fix_worked=entry.success,
                        success_rate=success_rate
                    )
                    similarities.append(similar)
            
            self.logger.info(
                f"Retrieved {len(similarities)} similar past errors "
                f"(best match: {similarities[0].similarity_score:.3f})"
            )
            
            return similarities
        
        except Exception as e:
            self.logger.error(f"Error retrieving similar memories: {e}")
            return []
    
    def get_success_rate(self, fix_type: str) -> float:
        """
        Get historical success rate for a fix type.
        
        Args:
            fix_type: Type of fix
            
        Returns:
            Success rate [0, 1]
        """
        return self.success_rates.get(fix_type, 0.5)
    
    def get_fix_statistics(self, fix_type: str) -> Dict[str, Any]:
        """
        Get statistics for a fix type.
        
        Args:
            fix_type: Type of fix
            
        Returns:
            Statistics dictionary
        """
        return self.fix_statistics.get(fix_type, {
            "attempts": 0,
            "successes": 0,
            "success_rate": 0.5,
            "avg_time_seconds": 0.0
        })
    
    def save(self, 
             json_path: str = MEMORY_DB_PATH,
             faiss_path: str = FAISS_INDEX_PATH) -> None:
        """
        Persist memory to disk.
        
        Args:
            json_path: Path for JSON metadata store
            faiss_path: Path for FAISS index
        """
        try:
            # Save JSON metadata
            metadata = {
                "entries": [entry.to_dict() for entry in self.memory_entries],
                "success_rates": self.success_rates,
                "fix_statistics": self.fix_statistics,
                "timestamp": datetime.now().isoformat()
            }
            
            Path(json_path).parent.mkdir(parents=True, exist_ok=True)
            with open(json_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Saved memory metadata to {json_path}")
            
            # Save FAISS index
            if self.faiss_index is not None:
                Path(faiss_path).parent.mkdir(parents=True, exist_ok=True)
                faiss.write_index(self.faiss_index, faiss_path)
                self.logger.info(f"Saved FAISS index to {faiss_path}")
        
        except Exception as e:
            self.logger.error(f"Error saving memory: {e}")
    
    def load(self,
             json_path: str = MEMORY_DB_PATH,
             faiss_path: str = FAISS_INDEX_PATH) -> None:
        """
        Load memory from disk.
        
        Args:
            json_path: Path to JSON metadata store
            faiss_path: Path to FAISS index
        """
        try:
            # Load JSON metadata
            if Path(json_path).exists():
                with open(json_path, 'r') as f:
                    metadata = json.load(f)
                
                # Restore entries
                self.memory_entries = [
                    MemoryEntry(
                        error_type=e["error_type"],
                        error_message=e["error_message"],
                        code_snippet=e["code_snippet"],
                        fix_applied=e["fix_applied"],
                        success=e["success"],
                        timestamp=e["timestamp"],
                        fix_time_seconds=e["fix_time_seconds"],
                        attempts=e["attempts"]
                    )
                    for e in metadata.get("entries", [])
                ]
                
                # Restore statistics
                self.success_rates = metadata.get("success_rates", {})
                self.fix_statistics = metadata.get("fix_statistics", {})
                
                self.logger.info(
                    f"Loaded {len(self.memory_entries)} memory entries "
                    f"from {json_path}"
                )
            
            # Load FAISS index
            if Path(faiss_path).exists() and faiss is not None:
                self.faiss_index = faiss.read_index(faiss_path)
                self.logger.info(f"Loaded FAISS index from {faiss_path}")
        
        except Exception as e:
            self.logger.error(f"Error loading memory: {e}")
    
    def _rebuild_faiss_index(self) -> None:
        """Rebuild FAISS index from current embeddings"""
        if not self.memory_entries or faiss is None:
            return
        
        try:
            # Extract embeddings from entries
            # For now, use simple heuristic; in production would use vectorizer
            embeddings = self._generate_embeddings()
            
            if embeddings is None:
                self.logger.warning("Could not generate embeddings")
                return
            
            # Create new FAISS index
            embeddings_float32 = embeddings.astype('float32')
            self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)
            self.faiss_index.add(embeddings_float32)
            
            self.logger.info(
                f"Rebuilt FAISS index with {len(embeddings)} vectors"
            )
        
        except Exception as e:
            self.logger.error(f"Error rebuilding FAISS index: {e}")
    
    def _generate_embeddings(self) -> Optional[np.ndarray]:
        """
        Generate embeddings for stored entries.
        
        In production, would use actual TF-IDF vectorizer.
        For now, uses simplified heuristic.
        
        Returns:
            Embeddings array or None
        """
        if not self.memory_entries:
            return None
        
        try:
            # Simplified embedding: bag-of-words with error type weighting
            embeddings = []
            
            for entry in self.memory_entries:
                # Create simple embedding
                embedding = np.zeros(self.embedding_dim)
                
                # Weight by error type
                error_type_hash = hash(entry.error_type) % self.embedding_dim
                embedding[error_type_hash] = 1.0
                
                # Weight by fix type
                fix_type_hash = hash(
                    entry.fix_applied['fix_type']
                ) % self.embedding_dim
                embedding[fix_type_hash] = 0.8
                
                # Weight by first few words of message
                for i, word in enumerate(entry.error_message.split()[:5]):
                    word_hash = hash(word) % self.embedding_dim
                    embedding[word_hash] += 0.3
                
                # Normalize
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    embedding = embedding / norm
                
                embeddings.append(embedding)
            
            return np.array(embeddings, dtype='float32')
        
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return None
    
    def _update_statistics(self, fix_type: str, success: bool, fix_time: float) -> None:
        """Update success statistics for a fix type"""
        if fix_type not in self.fix_statistics:
            self.fix_statistics[fix_type] = {
                "attempts": 0,
                "successes": 0,
                "total_time": 0.0,
                "avg_time_seconds": 0.0
            }
        
        stats = self.fix_statistics[fix_type]
        stats["attempts"] += 1
        if success:
            stats["successes"] += 1
        stats["total_time"] += fix_time
        stats["avg_time_seconds"] = stats["total_time"] / stats["attempts"]
        
        # Update success rate
        self.success_rates[fix_type] = (
            stats["successes"] / stats["attempts"]
            if stats["attempts"] > 0 else 0.5
        )
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get overall memory statistics"""
        total_entries = len(self.memory_entries)
        total_successes = sum(1 for e in self.memory_entries if e.success)
        
        return {
            "total_entries": total_entries,
            "total_successes": total_successes,
            "overall_success_rate": (
                total_successes / total_entries 
                if total_entries > 0 else 0
            ),
            "fix_types_tracked": len(self.fix_statistics),
            "avg_fix_time": (
                sum(e.fix_time_seconds for e in self.memory_entries) 
                / total_entries 
                if total_entries > 0 else 0
            )
        }


# ============================================================================
# INTEGRATION WITH AGENT LOOP
# ============================================================================

def integrate_memory_into_ranking(
    ranked_fixes: List['RankedFix'],
    similar_memories: List[SimilarMemory],
    memory_weight: float = 0.15
) -> List['RankedFix']:
    """
    Boost ranking of fixes based on similar past success.
    
    Args:
        ranked_fixes: Current ranked fixes
        similar_memories: Similar past errors retrieved
        memory_weight: Weight to apply from memory (0-1)
        
    Returns:
        Re-ranked fixes with memory influence
    """
    if not similar_memories:
        return ranked_fixes
    
    # Find best similar memory that succeeded
    successful_memories = [m for m in similar_memories if m.fix_worked]
    if not successful_memories:
        return ranked_fixes
    
    best_memory = max(successful_memories, key=lambda m: m.similarity_score)
    
    # Boost fixes matching the successful fix type
    boosted_fixes = []
    for rf in ranked_fixes:
        if rf.fix.fix_type.value == best_memory.entry.fix_applied['fix_type']:
            # Boost this fix's score
            boost = memory_weight * best_memory.similarity_score * 100
            rf.ranking_score += boost
        
        boosted_fixes.append(rf)
    
    # Re-sort by boosted scores
    boosted_fixes.sort(key=lambda x: x.ranking_score, reverse=True)
    
    return boosted_fixes


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Demo: Create and use semantic memory
    memory = SemanticMemory()
    
    # Simulate storing error-fix patterns
    from planning_module import FixStrategy, FixType
    
    fix = FixStrategy(
        fix_type=FixType.TYPE_CONVERSION,
        description="Convert types before operation",
        code_change="Use str() or int() to convert",
        complexity=1,
        confidence=0.92,
        reasoning="Type mismatch"
    )
    
    memory.store_error_fix(
        error_type="TypeError",
        error_message="unsupported operand type",
        code_snippet="x = 5 + 'hello'",
        fix=fix,
        success=True,
        fix_time=2.5,
        attempts=1
    )
    
    # Get statistics
    stats = memory.get_memory_stats()
    print("\nMemory Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Success rate: {stats['overall_success_rate']:.2%}")
    print(f"  Avg fix time: {stats['avg_fix_time']:.2f}s")
