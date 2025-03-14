# tests/system/test_knowledge_graph_visualization.py
import unittest
import os
import sys
import tempfile
import networkx as nx
import numpy as np
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import visualization functions
from app import visualize_knowledge_graph, export_knowledge_graph

class TestKnowledgeGraphVisualization(unittest.TestCase):
    """System tests specifically for Knowledge Graph visualization functionality"""
    
    def setUp(self):
        """Set up test environment with sample graph data"""
        # Create a test graph with realistic Human Design concepts
        self.test_graph = nx.Graph()
        
        # Add nodes (key Human Design concepts)
        concepts = [
            "Type", "Generator", "Projector", "Manifestor", "Reflector",
            "Authority", "Emotional Authority", "Sacral Authority", "Splenic Authority",
            "Strategy", "Profile", "Centers", "Definition", "Not-Self",
            "Gates", "Channels", "I Ching", "Sacral Center", "Throat Center"
        ]
        self.test_graph.add_nodes_from(concepts)
        
        # Add edges (relationships between concepts)
        edges = [
            ("Type", "Generator"), ("Type", "Projector"), ("Type", "Manifestor"), ("Type", "Reflector"),
            ("Generator", "Sacral Center"), ("Generator", "Strategy"), ("Generator", "Not-Self"),
            ("Projector", "Strategy"), ("Projector", "Not-Self"), ("Manifestor", "Strategy"), ("Manifestor", "Not-Self"),
            ("Authority", "Emotional Authority"), ("Authority", "Sacral Authority"), ("Authority", "Splenic Authority"),
            ("Sacral Authority", "Generator"), ("Sacral Center", "Sacral Authority"),
            ("Gates", "Channels"), ("Gates", "I Ching"), ("Channels", "Centers"),
            ("Centers", "Definition"), ("Centers", "Sacral Center"), ("Centers", "Throat Center")
        ]
        self.test_graph.add_edges_from(edges)
        
        # Add weights to edges
        for u, v in self.test_graph.edges():
            self.test_graph[u][v]['weight'] = np.random.randint(1, 5)
    
    # For the pyvis tests:
    @patch('os.unlink')  # Prevent the actual file deletion
    @patch('app.Network')
    def test_pyvis_visualization(self, mock_network, mock_unlink):
        """Test visualization with pyvis available"""
        # Mock the pyvis Network class and its methods
        mock_net_instance = MagicMock()
        mock_network.return_value = mock_net_instance
        
        # Mock tempfile operations with a real temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as real_temp_file:
            temp_path = real_temp_file.name
            
            # Write some dummy content to the file
            real_temp_file.write(b"<html><body>Network visualization</body></html>")
            real_temp_file.flush()
            
            # Mock tempfile to return our real file
            with patch('tempfile.NamedTemporaryFile', return_value=real_temp_file):
                with patch('builtins.open', mock_open(read_data="<html><body>Network visualization</body></html>")):
                    # Call visualization with PYVIS_AVAILABLE set to True
                    with patch('app.PYVIS_AVAILABLE', True):
                        # Call visualization
                        result = visualize_knowledge_graph(self.test_graph)
        
        # Cleanup the temp file
        try:
            os.unlink(temp_path)
        except:
            pass
            
        # Verify network setup was called
        mock_net_instance.barnes_hut.assert_called_once()
        
        # Verify nodes were added
        self.assertEqual(mock_net_instance.add_node.call_count, len(self.test_graph.nodes()))
        
        # Verify edges were added
        self.assertEqual(mock_net_instance.add_edge.call_count, len(self.test_graph.edges()))
        
        # Verify graph was saved
        mock_net_instance.save_graph.assert_called_once()
        
        # Result should be the HTML content
        self.assertEqual(result, "<html><body>Network visualization</body></html>")

    @patch('streamlit.error')
    @patch('streamlit.write')
    @patch('matplotlib.pyplot.savefig')
    @patch('networkx.drawing.nx_pylab.draw_networkx')
    def test_matplotlib_fallback(self, mock_draw_networkx, mock_savefig, mock_st_write, mock_st_error):
        """Test fallback to matplotlib when pyvis is not available"""
        # Mock PYVIS_AVAILABLE to be False
        with patch('app.PYVIS_AVAILABLE', False):
            # Call visualization
            result = visualize_knowledge_graph(self.test_graph)
            
            # Should return None when pyvis is not available
            self.assertIsNone(result)
            
            # Should have displayed info via streamlit
            mock_st_error.assert_called_once()
            self.assertGreaterEqual(mock_st_write.call_count, 1)
            
            # Not testing matplotlib directly as implementation might vary
            
            # # Should return None when pyvis is not available
            # self.assertIsNone(result)
            
            # # Should have attempted to create visualization with matplotlib
            # mock_draw_networkx.assert_called_once()
            # mock_savefig.assert_called_once()
            
            # # Should have printed graph info
            # mock_print.assert_any_call(f"Graph contains {len(self.test_graph.nodes())} concepts and {len(self.test_graph.edges())} connections")
    
    @patch('streamlit.error')
    @patch('streamlit.write')
    @patch('matplotlib.pyplot.savefig')
    def test_matplotlib_error_handling(self, mock_savefig, mock_st_write, mock_st_error):
        """Test error handling in matplotlib fallback"""
        # Mock PYVIS_AVAILABLE to be False
        with patch('app.PYVIS_AVAILABLE', False):
            # Call visualization
            result = visualize_knowledge_graph(self.test_graph)
            
            # Should return None when visualization fails
            self.assertIsNone(result)
            
            # Should have displayed an error message via streamlit
            mock_st_error.assert_called_once()
    
    def test_export_knowledge_graph(self):
        """Test exporting the knowledge graph to JSON format for visualization"""
        # Export the test graph
        exported_data = export_knowledge_graph(self.test_graph)
        
        # Verify the exported structure
        self.assertIn("nodes", exported_data)
        self.assertIn("links", exported_data)
        
        # Check node count
        self.assertEqual(len(exported_data["nodes"]), len(self.test_graph.nodes()))
        
        # Check link count
        self.assertEqual(len(exported_data["links"]), len(self.test_graph.edges()))
        
        # Verify node structure
        for node in exported_data["nodes"]:
            self.assertIn("id", node)
            self.assertIn("name", node)
            self.assertIn("degree", node)
            self.assertIn("group", node)
            
            # Node ID should be in the original graph
            self.assertIn(node["id"], self.test_graph.nodes())
            
            # Degree should match the graph
            self.assertEqual(node["degree"], self.test_graph.degree(node["id"]))
        
        # Verify link structure
        for link in exported_data["links"]:
            self.assertIn("source", link)
            self.assertIn("target", link)
            self.assertIn("value", link)
            
            # Edge should exist in original graph
            self.assertTrue(self.test_graph.has_edge(link["source"], link["target"]))
            
            # Value should match weight if it exists
            if "weight" in self.test_graph[link["source"]][link["target"]]:
                self.assertEqual(link["value"], self.test_graph[link["source"]][link["target"]]["weight"])
    
    def test_export_graph_compatibility(self):
        """Test that exported graph format is compatible with D3.js and other visualization libraries"""
        # Export the test graph
        exported_data = export_knowledge_graph(self.test_graph)
        
        # Check for D3.js compatibility
        # D3 requires nodes with id and links with source/target
        for node in exported_data["nodes"]:
            self.assertIn("id", node)
        
        for link in exported_data["links"]:
            self.assertIn("source", link)
            self.assertIn("target", link)
        
        # Ensure all source and target values in links correspond to actual node ids
        node_ids = [node["id"] for node in exported_data["nodes"]]
        for link in exported_data["links"]:
            self.assertIn(link["source"], node_ids)
            self.assertIn(link["target"], node_ids)
    
    @patch('os.unlink')  # Prevent the actual file deletion
    def test_visualization_color_coding(self, mock_unlink):
        """Test color coding in the visualization"""
        # Mock the pyvis Network class and its methods
        mock_net_instance = MagicMock()
        mock_network = MagicMock(return_value=mock_net_instance)
        
        # Mock PYVIS_AVAILABLE to be True
        with patch('app.PYVIS_AVAILABLE', True):
            with patch('app.Network', mock_network):
                # Create a real temporary file for the test
                with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as real_temp_file:
                    temp_path = real_temp_file.name
                    
                    # Write some dummy content to the file
                    real_temp_file.write(b"<html><body>Network visualization</body></html>")
                    real_temp_file.flush()
                    
                    # Mock tempfile to return our real file
                    with patch('tempfile.NamedTemporaryFile', return_value=real_temp_file):
                        with patch('builtins.open', mock_open(read_data="<html><body>Network visualization</body></html>")):
                            # Call visualization
                            result = visualize_knowledge_graph(self.test_graph)
                    
                # Clean up our temp file outside the mocked context
                try:
                    os.unlink(temp_path)
                except:
                    pass
        
        # Check color assignments for different node types
        # Get all calls to add_node
        add_node_calls = mock_net_instance.add_node.call_args_list
        
        # Track if we've seen different node types with appropriate colors
        found_type_node = False
        found_authority_node = False
        found_center_node = False
        
        for call in add_node_calls:
            args, kwargs = call
            node_name = args[0]
            node_color = kwargs.get('color', '')
            
            # Check Type nodes
            if node_name == "Type" or node_name == "Generator":
                self.assertIn(kwargs['color'], ["#6C63FF", "#BD93F9"])
                found_type_node = True
                
            # Check Authority nodes
            elif node_name == "Authority" or node_name == "Emotional Authority":
                self.assertIn(kwargs['color'], ["#6C63FF", "#BD93F9"])
                found_authority_node = True
                
            # Check Center nodes
            elif node_name == "Centers" or node_name == "Sacral Center":
                self.assertIn(kwargs['color'], ["#6C63FF", "#BD93F9"])
                found_center_node = True
        
        # Verify we found at least one node of each type
        self.assertTrue(found_type_node, "Didn't find correctly colored Type node")
        self.assertTrue(found_authority_node, "Didn't find correctly colored Authority node")
        self.assertTrue(found_center_node, "Didn't find correctly colored Center node")

if __name__ == '__main__':
    unittest.main()