import json
import numpy as np
import logging
from datetime import datetime, date
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

class PreswaldJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for Preswald data types."""
    
    def default(self, obj: Any) -> Any:
        """Convert object to JSON serializable format."""
        try:
            if isinstance(obj, np.ndarray):
                return self._handle_ndarray(obj)
            elif isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
                if np.isnan(obj):
                    return None
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, (set, frozenset)):
                return list(obj)
            elif isinstance(obj, bytes):
                return obj.decode('utf-8')
            elif isinstance(obj, np.void):
                return None
            return super().default(obj)
        except Exception as e:
            logger.error(f"Error encoding object {type(obj)}: {e}")
            return None

    def _handle_ndarray(self, arr: np.ndarray) -> Union[List, None]:
        """Handle numpy array conversion."""
        try:
            if arr.dtype.kind in ['U', 'S']:  # Unicode or string
                return arr.astype(str).tolist()
            elif arr.dtype.kind == 'M':  # Datetime
                return arr.astype(str).tolist()
            elif arr.dtype.kind == 'm':  # Timedelta
                return arr.astype('timedelta64[ns]').astype(np.int64).tolist()
            elif arr.dtype.kind == 'O':  # Object
                return [self.default(x) for x in arr]
            else:
                return self._handle_array_values(arr.tolist())
        except Exception as e:
            logger.error(f"Error handling ndarray: {e}")
            return None

    def _handle_array_values(self, arr: List) -> List:
        """Handle array values recursively."""
        if isinstance(arr, (list, tuple)):
            return [self._handle_array_values(x) for x in arr]
        elif isinstance(arr, (float, np.float_, np.float16, np.float32, np.float64)):
            if np.isnan(arr):
                return None
            return float(arr)
        elif isinstance(arr, (int, np.integer)):
            return int(arr)
        elif isinstance(arr, (str, bool)):
            return arr
        elif arr is None:
            return None
        else:
            try:
                return self.default(arr)
            except:
                return str(arr)

def dumps(obj: Any, **kwargs) -> str:
    """
    Serialize obj to a JSON formatted str using the custom encoder.
    
    Args:
        obj: The object to serialize
        **kwargs: Additional arguments to pass to json.dumps
    
    Returns:
        JSON formatted string
    """
    try:
        return json.dumps(obj, cls=PreswaldJSONEncoder, **kwargs)
    except Exception as e:
        logger.error(f"Error serializing object: {e}")
        # Return a safe fallback
        return json.dumps({
            "error": "Serialization failed",
            "message": str(e)
        })

def loads(s: str, **kwargs) -> Any:
    """
    Deserialize s (a str instance containing a JSON document) to a Python object.
    
    Args:
        s: The JSON string to deserialize
        **kwargs: Additional arguments to pass to json.loads
    
    Returns:
        Deserialized Python object
    """
    try:
        return json.loads(s, **kwargs)
    except Exception as e:
        logger.error(f"Error deserializing JSON: {e}")
        return None 