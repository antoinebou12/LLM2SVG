import os
import re
import glob
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict, Counter
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

from utils.data_loader import SVGDataLoader
from utils.svg_constraints import SVGConstraints

class SVGAnalyzer:
    """Utility for analyzing SVG files in the dataset"""
    
    def __init__(self, data_dir: str = "/c:/Users/antoi/LLM2SVG/data"):
        """
        Initialize the SVG analyzer.
        
        Args:
            data_dir: Base directory containing the data
        """
        self.data_loader = SVGDataLoader(data_dir)
        self.svg_validator = SVGConstraints()
    
    def count_svgs(self, split: str = "train") -> Dict[str, int]:
        """
        Count the number of SVG files for each sample.
        
        Args:
            split: Dataset split ("train" or "test")
            
        Returns:
            Dictionary mapping sample IDs to SVG counts
        """
        svg_paths = self.data_loader.get_svg_paths(split)
        return {sample_id: len(paths) for sample_id, paths in svg_paths.items()}
    
    def get_svg_sizes(self, split: str = "train") -> Dict[str, Dict[str, int]]:
        """
        Get the file sizes of all SVG files.
        
        Args:
            split: Dataset split ("train" or "test")
            
        Returns:
            Dictionary mapping sample IDs to dictionaries of SVG file names to sizes in bytes
        """
        svg_paths = self.data_loader.get_svg_paths(split)
        svg_sizes = {}
        
        for sample_id, paths in svg_paths.items():
            svg_sizes[sample_id] = {}
            for path in paths:
                try:
                    file_size = os.path.getsize(path)
                    file_name = os.path.basename(path)
                    svg_sizes[sample_id][file_name] = file_size
                except Exception as e:
                    print(f"Error getting size of {path}: {e}")
        
        return svg_sizes
    
    def analyze_elements(self, split: str = "train") -> Dict[str, Counter]:
        """
        Analyze the elements used in SVG files.
        
        Args:
            split: Dataset split ("train" or "test")
            
        Returns:
            Dictionary mapping sample IDs to counters of element types
        """
        svg_contents = self.data_loader.load_all_svgs(split)
        element_counts = {}
        
        for sample_id, svgs in svg_contents.items():
            element_counts[sample_id] = Counter()
            for file_name, content in svgs.items():
                try:
                    # Use regex instead of XML parsing to handle potentially invalid SVGs
                    elements = re.findall(r'<(\w+)[ >]', content)
                    element_counts[sample_id].update(elements)
                except Exception as e:
                    print(f"Error analyzing elements in {sample_id}/{file_name}: {e}")
        
        return element_counts
    
    def validate_all_svgs(self, split: str = "train") -> Dict[str, Dict[str, bool]]:
        """
        Validate all SVGs against the constraints.
        
        Args:
            split: Dataset split ("train" or "test")
            
        Returns:
            Dictionary mapping sample IDs to dictionaries of SVG file names to validation results
        """
        svg_contents = self.data_loader.load_all_svgs(split)
        validation_results = {}
        
        for sample_id, svgs in svg_contents.items():
            validation_results[sample_id] = {}
            for file_name, content in svgs.items():
                try:
                    self.svg_validator.validate_svg(content)
                    validation_results[sample_id][file_name] = True
                except ValueError as e:
                    print(f"Invalid SVG in {sample_id}/{file_name}: {e}")
                    validation_results[sample_id][file_name] = False
        
        return validation_results
    
    def generate_summary_report(self, split: str = "train", output_path: Optional[str] = None) -> pd.DataFrame:
        """
        Generate a summary report of the SVG dataset.
        
        Args:
            split: Dataset split ("train" or "test")
            output_path: Optional path to save the report CSV
            
        Returns:
            DataFrame containing the summary report
        """
        svg_paths = self.data_loader.get_svg_paths(split)
        svg_sizes = self.get_svg_sizes(split)
        
        # Get descriptions
        descriptions = self.data_loader.get_train_descriptions() if split == "train" else self.data_loader.get_test_descriptions()
        
        # Prepare data for report
        report_data = []
        for sample_id, paths in svg_paths.items():
            for path in paths:
                file_name = os.path.basename(path)
                size = svg_sizes.get(sample_id, {}).get(file_name, 0)
                
                row = {
                    'sample_id': sample_id,
                    'file_name': file_name,
                    'size_bytes': size,
                    'description': descriptions.get(sample_id, ""),
                    'source': self._infer_source_from_filename(file_name)
                }
                report_data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(report_data)
        
        # Save if output path provided
        if output_path:
            df.to_csv(output_path, index=False)
        
        return df
    
    def _infer_source_from_filename(self, file_name: str) -> str:
        """
        Infer the source of an SVG file from its filename.
        
        Args:
            file_name: Name of the SVG file
            
        Returns:
            Inferred source of the SVG
        """
        file_name_lower = file_name.lower()
        
        if "claude" in file_name_lower:
            return "claude"
        elif "gpt" in file_name_lower:
            return "gpt"
        elif "gemini" in file_name_lower:
            return "gemini"
        elif "stablediffusion" in file_name_lower:
            return "stablediffusion"
        elif "mistral" in file_name_lower:
            return "mistral"
        elif "qwen" in file_name_lower:
            return "qwen"
        elif "deepseek" in file_name_lower:
            return "deepseek"
        else:
            return "unknown"
    
    def plot_svg_size_distribution(self, split: str = "train", output_path: Optional[str] = None):
        """
        Plot the distribution of SVG file sizes.
        
        Args:
            split: Dataset split ("train" or "test")
            output_path: Optional path to save the plot
        """
        svg_sizes = self.get_svg_sizes(split)
        
        # Extract all sizes
        all_sizes = []
        for sample_sizes in svg_sizes.values():
            all_sizes.extend(sample_sizes.values())
        
        plt.figure(figsize=(10, 6))
        plt.hist(all_sizes, bins=50, alpha=0.7)
        plt.axvline(x=10000, color='r', linestyle='--', label='10KB limit')
        plt.xlabel('File Size (bytes)')
        plt.ylabel('Count')
        plt.title(f'SVG File Size Distribution ({split})')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
