"""
ML Classification Module
Classifies error types using TF-IDF vectorization and Logistic Regression.
Provides error type prediction with confidence scores.
"""

import json
import logging
import pickle
from typing import Tuple, List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

try:
    from config_settings import (
        TFIDF_MAX_FEATURES, TFIDF_MAX_DF, TFIDF_MIN_DF,
        TFIDF_NGRAM_RANGE, ERROR_TYPES, CONFIDENCE_THRESHOLD,
        VECTORIZER_MODEL_PATH, CLASSIFIER_MODEL_PATH, TRAINING_DIR
    )
except ImportError:
    # Default values if config not available
    TFIDF_MAX_FEATURES = 1000
    TFIDF_MAX_DF = 0.8
    TFIDF_MIN_DF = 2
    TFIDF_NGRAM_RANGE = (1, 2)
    ERROR_TYPES = [
        "SyntaxError", "TypeError", "ValueError", "RuntimeError",
        "LogicError", "IndexError", "KeyError", "AttributeError",
        "ImportError", "ZeroDivisionError", "IndentationError",
        "NameError", "UnboundLocalError"
    ]
    CONFIDENCE_THRESHOLD = 0.6
    VECTORIZER_MODEL_PATH = "models/vectorizer.pkl"
    CLASSIFIER_MODEL_PATH = "models/classifier.pkl"
    TRAINING_DIR = "data/training"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ClassificationResult:
    """Result of error classification"""
    predicted_type: str          # Predicted error type
    confidence: float            # Confidence score [0, 1]
    top_3_predictions: List[Tuple[str, float]]  # Top 3 with scores
    is_confident: bool           # Whether confidence >= threshold
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "predicted_type": self.predicted_type,
            "confidence": round(float(self.confidence), 4),
            "top_3_predictions": [
                (name, round(float(score), 4)) 
                for name, score in self.top_3_predictions
            ],
            "is_confident": self.is_confident
        }


# ============================================================================
# ERROR CLASSIFIER
# ============================================================================

class ErrorClassifier:
    """
    Machine learning-based error classifier.
    
    Uses TF-IDF vectorization + Logistic Regression to classify error types
    based on error message and context.
    
    Pipeline:
    1. Vectorize error text (TF-IDF)
    2. Predict error type (Logistic Regression)
    3. Get confidence score
    4. Return top predictions
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize classifier"""
        self.logger = logger or logging.getLogger(__name__)
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.classifier: Optional[LogisticRegression] = None
        self.label_encoder: Optional[LabelEncoder] = None
        self.is_trained = False
    
    def train(self, error_texts: List[str], error_types: List[str]) -> None:
        """
        Train the classifier on error examples.
        
        Args:
            error_texts: List of error descriptions/messages
            error_types: List of corresponding error type labels
        """
        self.logger.info(f"Training classifier on {len(error_texts)} examples")
        
        # Validate input
        if len(error_texts) != len(error_types):
            raise ValueError("Mismatch between texts and types")
        
        # Initialize vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=TFIDF_MAX_FEATURES,
            max_df=TFIDF_MAX_DF,
            min_df=TFIDF_MIN_DF,
            ngram_range=TFIDF_NGRAM_RANGE,
            lowercase=True,
            stop_words='english'
        )
        
        # Initialize label encoder
        self.label_encoder = LabelEncoder()
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(error_texts)
        self.logger.info(f"Vectorizer created with {X.shape[1]} features")
        
        # Encode labels
        y = self.label_encoder.fit_transform(error_types)
        
        # Train classifier
        self.classifier = LogisticRegression(
            max_iter=200,
            random_state=42,
            multi_class='multinomial',
            solver='lbfgs',
            class_weight='balanced'  # Handle imbalanced data
        )
        self.classifier.fit(X, y)
        
        self.is_trained = True
        self.logger.info("Classifier training completed")
        
        # Log accuracy
        train_accuracy = self.classifier.score(X, y)
        self.logger.info(f"Training accuracy: {train_accuracy:.4f}")
    
    def predict(self, error_text: str) -> ClassificationResult:
        """
        Predict error type for given error text.
        
        Args:
            error_text: Error message or description
            
        Returns:
            ClassificationResult with prediction and confidence
        """
        if not self.is_trained:
            self.logger.warning("Classifier not trained, loading from disk")
            self.load()
        
        # Vectorize input
        X = self.vectorizer.transform([error_text])
        
        # Get prediction
        pred_idx = self.classifier.predict(X)[0]
        pred_type = self.label_encoder.inverse_transform([pred_idx])[0]
        
        # Get confidence scores (probability)
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = float(probabilities[pred_idx])
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_predictions = [
            (
                self.label_encoder.inverse_transform([idx])[0],
                float(probabilities[idx])
            )
            for idx in top_3_indices
        ]
        
        is_confident = confidence >= CONFIDENCE_THRESHOLD
        
        return ClassificationResult(
            predicted_type=pred_type,
            confidence=confidence,
            top_3_predictions=top_3_predictions,
            is_confident=is_confident
        )
    
    def save(self, vectorizer_path: str = VECTORIZER_MODEL_PATH,
             classifier_path: str = CLASSIFIER_MODEL_PATH) -> None:
        """
        Save trained models to disk.
        
        Args:
            vectorizer_path: Path to save TF-IDF vectorizer
            classifier_path: Path to save classifier
        """
        if not self.is_trained:
            raise RuntimeError("Classifier not trained yet")
        
        # Save vectorizer
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        self.logger.info(f"Vectorizer saved to {vectorizer_path}")
        
        # Save label encoder
        encoder_path = classifier_path.replace('.pkl', '_encoder.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        self.logger.info(f"Label encoder saved to {encoder_path}")
        
        # Save classifier
        with open(classifier_path, 'wb') as f:
            pickle.dump(self.classifier, f)
        self.logger.info(f"Classifier saved to {classifier_path}")
    
    def load(self, vectorizer_path: str = VECTORIZER_MODEL_PATH,
             classifier_path: str = CLASSIFIER_MODEL_PATH) -> None:
        """
        Load trained models from disk.
        
        Args:
            vectorizer_path: Path to TF-IDF vectorizer
            classifier_path: Path to classifier
        """
        try:
            # Load vectorizer
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load label encoder
            encoder_path = classifier_path.replace('.pkl', '_encoder.pkl')
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            # Load classifier
            with open(classifier_path, 'rb') as f:
                self.classifier = pickle.load(f)
            
            self.is_trained = True
            self.logger.info("Models loaded successfully")
        
        except FileNotFoundError:
            self.logger.warning("Model files not found, initializing untrained classifier")
            self.is_trained = False
    
    def evaluate(self, error_texts: List[str], error_types: List[str]) -> Dict[str, Any]:
        """
        Evaluate classifier on test data.
        
        Args:
            error_texts: Test error descriptions
            error_types: Test labels
            
        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise RuntimeError("Classifier not trained")
        
        predictions = []
        for text in error_texts:
            result = self.predict(text)
            predictions.append(result.predicted_type)
        
        accuracy = accuracy_score(error_types, predictions)
        
        return {
            "accuracy": float(accuracy),
            "classification_report": classification_report(
                error_types, predictions, output_dict=True
            ),
            "confusion_matrix": confusion_matrix(
                error_types, predictions
            ).tolist()
        }


# ============================================================================
# TRAINING DATA LOADER
# ============================================================================

class TrainingDataLoader:
    """Load and manage training data for error classifier"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize loader"""
        self.logger = logger or logging.getLogger(__name__)
    
    def load_training_corpus(self, corpus_path: str) -> Tuple[List[str], List[str]]:
        """
        Load training corpus from JSON file.
        
        Expected format:
        {
            "errors": [
                {"text": "...", "type": "..."},
                ...
            ]
        }
        
        Args:
            corpus_path: Path to JSON file
            
        Returns:
            Tuple of (error_texts, error_types)
        """
        try:
            with open(corpus_path, 'r') as f:
                data = json.load(f)
            
            error_texts = []
            error_types = []
            
            for item in data.get("errors", []):
                error_texts.append(item["text"])
                error_types.append(item["type"])
            
            self.logger.info(f"Loaded {len(error_texts)} training examples")
            return error_texts, error_types
        
        except Exception as e:
            self.logger.error(f"Error loading training data: {e}")
            raise
    
    @staticmethod
    def create_sample_corpus() -> Tuple[List[str], List[str]]:
        """
        Create a sample training corpus for demonstration.
        
        Returns:
            Tuple of (error_texts, error_types)
        """
        error_texts = [
            # Syntax errors
            "SyntaxError: invalid syntax",
            "Expected ':' at end of line",
            "Unexpected token found",
            
            # Type errors
            "unsupported operand type(s) for +: 'int' and 'str'",
            "cannot concatenate 'str' and 'int' objects",
            "Type mismatch in operation",
            
            # Value errors
            "invalid literal for int() with base 10: 'abc'",
            "could not convert string to float",
            "Value out of expected range",
            
            # Name errors
            "name 'x' is not defined",
            "undefined variable used",
            "NameError: variable not in scope",
            
            # Index errors
            "list index out of range",
            "tuple index exceeds length",
            "index out of bounds",
            
            # Key errors
            "KeyError: 'missing_key'",
            "Dictionary key not found",
            "'key' is not in dictionary",
            
            # Attribute errors
            "has no attribute 'foo'",
            "AttributeError: object does not have attribute",
            "Method not found on object",
            
            # Zero division
            "division by zero",
            "ZeroDivisionError: integer division or modulo",
            "Cannot divide by zero",
            
            # Runtime errors (generic)
            "Runtime error occurred",
            "Execution failed unexpectedly",
            "Program crashed during execution",
            
            # Logic errors
            "Output does not match expected",
            "Algorithm produced wrong result",
            "Logic error in code flow",
        ]
        
        error_types = [
            # Syntax errors
            "SyntaxError", "SyntaxError", "SyntaxError",
            # Type errors
            "TypeError", "TypeError", "TypeError",
            # Value errors
            "ValueError", "ValueError", "ValueError",
            # Name errors
            "NameError", "NameError", "NameError",
            # Index errors
            "IndexError", "IndexError", "IndexError",
            # Key errors
            "KeyError", "KeyError", "KeyError",
            # Attribute errors
            "AttributeError", "AttributeError", "AttributeError",
            # Zero division
            "ZeroDivisionError", "ZeroDivisionError", "ZeroDivisionError",
            # Runtime errors
            "RuntimeError", "RuntimeError", "RuntimeError",
            # Logic errors
            "LogicError", "LogicError", "LogicError",
        ]
        
        return error_texts, error_types


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def train_classifier_from_corpus(corpus_path: str) -> ErrorClassifier:
    """Train classifier from corpus file"""
    loader = TrainingDataLoader()
    error_texts, error_types = loader.load_training_corpus(corpus_path)
    
    classifier = ErrorClassifier()
    classifier.train(error_texts, error_types)
    classifier.save()
    
    return classifier


def classify_error(error_text: str) -> ClassificationResult:
    """Classify a single error"""
    classifier = ErrorClassifier()
    return classifier.predict(error_text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create sample classifier
    loader = TrainingDataLoader()
    error_texts, error_types = loader.create_sample_corpus()
    
    classifier = ErrorClassifier()
    classifier.train(error_texts, error_types)
    
    # Test prediction
    test_error = "list index out of range at position 5"
    result = classifier.predict(test_error)
    
    print(f"\nTest error: {test_error}")
    print(f"Predicted type: {result.predicted_type}")
    print(f"Confidence: {result.confidence:.4f}")
    print(f"Top 3 predictions:")
    for err_type, conf in result.top_3_predictions:
        print(f"  - {err_type}: {conf:.4f}")
