from server import mcp
from utils.file_reader import read_parquet_summary

@mcp.tool()
def summaries_parquet_file(filename: str) -> str: 
    """
    Summarise a Parquet file by reporting the number of rows and columns
    
    Args: 
        filename: Name of the Parquet file in /data directory (e.g, sample.parquet)
        
    Returns: 
        A string describing the file's dimensions
    """
    return read_parquet_summary(filename)