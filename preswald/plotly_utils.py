import numpy as np
import json
import logging
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

def clean_nan_values(obj: Any) -> Any:
    """Clean NaN values from any object recursively."""
    if isinstance(obj, (float, np.floating)):
        return None if np.isnan(obj) else float(obj)
    elif isinstance(obj, (list, tuple)):
        return [clean_nan_values(x) for x in x if x is not None]
    elif isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, np.ndarray):
        if obj.dtype.kind in ['f', 'c']:  # Float or complex
            obj = np.where(np.isnan(obj), None, obj)
        return obj.tolist()
    return obj

def clean_plotly_data(fig_dict: Dict) -> Dict:
    """Clean plotly figure data to ensure JSON serialization."""
    try:
        # Clean data traces
        if 'data' in fig_dict:
            for trace in fig_dict['data']:
                # Clean marker properties
                if isinstance(trace.get('marker'), dict):
                    marker = trace['marker']
                    # Handle sizeref
                    if 'sizeref' in marker:
                        marker['sizeref'] = clean_nan_values(marker['sizeref'])
                    # Handle color array
                    if 'color' in marker:
                        marker['color'] = clean_nan_values(marker['color'])
                    # Handle size array
                    if 'size' in marker:
                        marker['size'] = clean_nan_values(marker['size'])
                
                # Clean coordinate arrays
                for coord in ['x', 'y', 'z', 'lat', 'lon']:
                    if coord in trace:
                        trace[coord] = clean_nan_values(trace[coord])
                
                # Clean text arrays
                if 'text' in trace:
                    trace['text'] = clean_nan_values(trace['text'])
                
                # Clean hover text
                if 'hovertext' in trace:
                    trace['hovertext'] = clean_nan_values(trace['hovertext'])

        # Clean layout
        if 'layout' in fig_dict:
            fig_dict['layout'] = clean_nan_values(fig_dict['layout'])

        return fig_dict
    except Exception as e:
        logger.error(f"Error cleaning plotly data: {e}")
        return fig_dict

def convert_figure_to_json(fig: Any) -> Dict:
    """Convert a plotly figure to JSON-safe format."""
    try:
        # Convert figure to dict
        fig_dict = fig.to_dict()
        
        # Clean NaN values
        cleaned_dict = clean_plotly_data(fig_dict)
        
        # Create component data
        component_data = {
            "data": cleaned_dict.get("data", []),
            "layout": cleaned_dict.get("layout", {}),
            "config": {
                "responsive": True,
                "displayModeBar": True,
                "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                "displaylogo": False
            }
        }
        
        # Verify JSON serialization
        json.dumps(component_data)
        
        return component_data
    except Exception as e:
        logger.error(f"Error converting figure to JSON: {e}")
        return {
            "error": str(e),
            "data": [],
            "layout": {},
            "config": {}
        } 