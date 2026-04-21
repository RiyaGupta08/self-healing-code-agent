"""
Configuration Settings for Self-Healing Code Agent
Centralized configuration management for all components.
"""

import os
from pathlib import Path
from typing import Final

# ============================================================================
# PATHS & DIRECTORIES
# ============================================================================

PROJECT_ROOT: Final[Path] = Path(__file__).parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
MODELS_DIR: Final[Path] = DATA_DIR / "models"
LOGS_DIR: Final[Path] = DATA_DIR / "logs"
TRAINING_DIR: Final[Path] = DATA_DIR / "training"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR, TRAINING_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_FILE: Final[str] = str(LOGS_DIR / "agent_logs.log")
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# ============================================================================
# ERROR DETECTION CONFIGURATION
# ============================================================================

# Static analysis
ENABLE_STATIC_ANALYSIS: Final[bool] = True
ENABLE_TYPE_CHECKING: Final[bool] = True

# Runtime detection
EXECUTION_TIMEOUT_SECONDS: Final[int] = 5
MAX_MEMORY_MB: Final[int] = 512
MAX_OUTPUT_CHARS: Final[int] = 10000

# ============================================================================
# ML CLASSIFICATION CONFIGURATION
# ============================================================================

# TF-IDF Vectorizer
TFIDF_MAX_FEATURES: Final[int] = 1000
TFIDF_MAX_DF: Final[float] = 0.8
TFIDF_MIN_DF: Final[int] = 2
TFIDF_NGRAM_RANGE: Final[tuple] = (1, 2)

# Classifier
CLASSIFIER_MODEL_PATH: Final[str] = str(MODELS_DIR / "classifier.pkl")
VECTORIZER_MODEL_PATH: Final[str] = str(MODELS_DIR / "vectorizer.pkl")
CONFIDENCE_THRESHOLD: Final[float] = 0.6  # Only use if confidence > 60%

# Error types for classification
ERROR_TYPES: Final[list] = [
    "SyntaxError",
    "TypeError",
    "ValueError",
    "RuntimeError",
    "LogicError",
    "IndexError",
    "KeyError",
    "AttributeError",
    "ImportError",
    "ZeroDivisionError",
    "IndentationError",
    "NameError",
    "UnboundLocalError",
]

# ============================================================================
# PLANNING & FIX GENERATION CONFIGURATION
# ============================================================================

MAX_FIXES_TO_GENERATE: Final[int] = 5
MAX_FIXES_TO_TRY: Final[int] = 3

# Fix ranking weights
WEIGHT_ML_CONFIDENCE: Final[float] = 0.40
WEIGHT_HISTORICAL_SUCCESS: Final[float] = 0.40
WEIGHT_COMPLEXITY: Final[float] = 0.20

# Complexity scores (lower is better)
COMPLEXITY_SIMPLE: Final[int] = 1
COMPLEXITY_MEDIUM: Final[int] = 2
COMPLEXITY_HIGH: Final[int] = 3

# ============================================================================
# SEMANTIC MEMORY CONFIGURATION
# ============================================================================

# FAISS
FAISS_INDEX_PATH: Final[str] = str(MODELS_DIR / "faiss_index.bin")
EMBEDDING_DIMENSION: Final[int] = 1000  # TF-IDF dimensions
TOP_K_MEMORIES: Final[int] = 5  # Retrieve top 5 similar errors

# Memory storage
MEMORY_DB_PATH: Final[str] = str(DATA_DIR / "memory_store.json")
MAX_MEMORY_SIZE: Final[int] = 10000  # Maximum errors to store

# ============================================================================
# EXECUTION & SANDBOX CONFIGURATION
# ============================================================================

# Sandbox type: "subprocess" or "docker"
SANDBOX_TYPE: Final[str] = os.getenv("SANDBOX_TYPE", "subprocess")

# Docker configuration (if using Docker sandbox)
DOCKER_IMAGE: Final[str] = "python:3.11-slim"
DOCKER_NETWORK: Final[str] = "none"  # Disable network for security

# Subprocess configuration
SUBPROCESS_PREEXEC_FN: Final[bool] = True  # Use resource limits on Unix

# ============================================================================
# TEST VALIDATION CONFIGURATION
# ============================================================================

# Pytest
PYTEST_TIMEOUT: Final[int] = 10
ENABLE_TEST_COVERAGE: Final[bool] = True
COVERAGE_THRESHOLD: Final[float] = 0.70

# Test detection
AUTO_DETECT_TESTS: Final[bool] = True
TEST_FILE_PATTERNS: Final[list] = ["test_*.py", "*_test.py"]

# ============================================================================
# AGENT LOOP CONFIGURATION
# ============================================================================

MAX_RETRY_ATTEMPTS: Final[int] = 3
AGENT_TIMEOUT_SECONDS: Final[int] = 300  # 5 minutes max per error

# Success criteria
SUCCESS_ON_NO_ERROR: Final[bool] = True
SUCCESS_ON_ALL_TESTS_PASS: Final[bool] = True

# ============================================================================
# STREAMLIT UI CONFIGURATION
# ============================================================================

STREAMLIT_THEME: Final[str] = "dark"
STREAMLIT_LAYOUT: Final[str] = "wide"
STREAMLIT_MAX_UPLOADER_SIZE_MB: Final[int] = 10

# ============================================================================
# FEATURE FLAGS
# ============================================================================

ENABLE_MEMORY_LEARNING: Final[bool] = True
ENABLE_ML_RANKING: Final[bool] = True
ENABLE_SANDBOX_EXECUTION: Final[bool] = True
ENABLE_TEST_VALIDATION: Final[bool] = True
ENABLE_DETAILED_LOGGING: Final[bool] = True

# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

# Caching
ENABLE_ERROR_CACHE: Final[bool] = True
CACHE_SIZE_MB: Final[int] = 100

# Parallel processing (future)
ENABLE_PARALLEL_FIX_TESTING: Final[bool] = False
NUM_WORKERS: Final[int] = 2

# ============================================================================
# DEBUG & DEVELOPMENT
# ============================================================================

DEBUG_MODE: Final[bool] = os.getenv("DEBUG", "False").lower() == "true"
DRY_RUN_MODE: Final[bool] = False  # Don't actually apply fixes
VERBOSE_OUTPUT: Final[bool] = True
SAVE_ALL_ATTEMPTS: Final[bool] = True  # Save every fix attempt to logs
