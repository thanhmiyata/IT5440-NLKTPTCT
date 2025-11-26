"""
Dynamic Slicer - Concept 2: Dynamic Slicing
============================================
Implements dynamic program slicing using backward traversal algorithm.
Computes the slice of a program based on a target variable at a target line.
"""

from typing import Set, List, Dict, Any, Tuple
from dataclasses import dataclass
import re


@dataclass
class SliceResult:
    """Result of a dynamic slicing operation"""
    target_line: int
    target_var: str
    relevant_lines: Set[int]
    data_dependencies: Dict[int, Set[str]]  # line -> variables it depends on
    control_dependencies: Dict[int, Set[int]]  # line -> lines that control it
    
    def __repr__(self):
        return (f"SliceResult(target={self.target_var}@L{self.target_line}, "
                f"relevant_lines={sorted(self.relevant_lines)})")


class DynamicSlicer:
    """
    Dynamic Slicer that computes program slices using backward traversal.
    
    Algorithm:
    1. Start from target_line with target_var
    2. Find the last writer to target_var
    3. Trace back data dependencies (variables used to define target_var)
    4. Trace back control dependencies (conditions that controlled execution)
    """
    
    def __init__(self):
        self.relevant_lines: Set[int] = set()
        self.variables_of_interest: Set[str] = set()
        self.data_deps: Dict[int, Set[str]] = {}
        self.control_deps: Dict[int, Set[int]] = {}
        
    def compute_dynamic_slice(self, 
                             execution_trace: List,
                             target_line: int,
                             target_var: str) -> SliceResult:
        """
        Compute the dynamic slice for a target variable at a target line.
        
        Args:
            execution_trace: List of TraceEvent objects from Tracer
            target_line: Line number of interest
            target_var: Variable name of interest
            
        Returns:
            SliceResult containing relevant lines and dependencies
        """
        # Reset state
        self.relevant_lines = set()
        self.variables_of_interest = {target_var}
        self.data_deps = {}
        self.control_deps = {}
        
        # Find the target event in the trace
        target_event_idx = self._find_target_event(execution_trace, target_line, target_var)
        
        if target_event_idx is None:
            print(f"Warning: Could not find target variable '{target_var}' at line {target_line}")
            return SliceResult(
                target_line=target_line,
                target_var=target_var,
                relevant_lines=set(),
                data_dependencies={},
                control_dependencies={}
            )
        
        # Backward traversal from target
        self._backward_traverse(execution_trace, target_event_idx)
        
        return SliceResult(
            target_line=target_line,
            target_var=target_var,
            relevant_lines=self.relevant_lines,
            data_dependencies=self.data_deps,
            control_dependencies=self.control_deps
        )
    
    def _find_target_event(self, trace: List, target_line: int, target_var: str) -> int:
        """Find the last occurrence of target_var at target_line in the trace"""
        for i in range(len(trace) - 1, -1, -1):
            event = trace[i]
            if event.line_number == target_line and target_var in event.local_vars:
                return i
        return None
    
    def _backward_traverse(self, trace: List, start_idx: int):
        """
        Perform backward traversal to find all relevant lines.
        
        Args:
            trace: Execution trace
            start_idx: Index to start backward traversal from
        """
        # Process events in reverse order
        for i in range(start_idx, -1, -1):
            event = trace[i]
            line = event.line_number
            
            # Check if this line affects any variable of interest
            affected_vars = self._get_affected_variables(event)
            
            # Check for data dependencies
            for var in affected_vars:
                if var in self.variables_of_interest:
                    # This line is relevant
                    self.relevant_lines.add(line)
                    
                    # Find variables used to compute this variable
                    used_vars = self._extract_used_variables(event, var)
                    
                    # Add data dependencies
                    if line not in self.data_deps:
                        self.data_deps[line] = set()
                    self.data_deps[line].update(used_vars)
                    
                    # Add used variables to variables of interest
                    self.variables_of_interest.update(used_vars)
            
            # Check for control dependencies
            if self._is_control_statement(event):
                # If this is a control statement (if, while, for)
                # and it affects our execution path, it's relevant
                control_vars = self._extract_control_variables(event)
                if control_vars & self.variables_of_interest:
                    self.relevant_lines.add(line)
                    
                    # Add control dependency
                    for relevant_line in list(self.relevant_lines):
                        if relevant_line > line:  # Lines controlled by this statement
                            if relevant_line not in self.control_deps:
                                self.control_deps[relevant_line] = set()
                            self.control_deps[relevant_line].add(line)
    
    def _get_affected_variables(self, event) -> Set[str]:
        """Get variables that were written/modified in this event"""
        affected = set()
        for access in event.memory_access:
            if access.startswith('write:'):
                var_name = access.split(':', 1)[1]
                affected.add(var_name)
        return affected
    
    def _extract_used_variables(self, event, target_var: str) -> Set[str]:
        """
        Extract variables used to compute target_var at this event.
        This is a simplified version - in reality, would need AST analysis.
        """
        used_vars = set()
        
        # Look at all variables in the local scope
        for var_name in event.local_vars:
            # Skip the target variable itself and special variables
            if var_name != target_var and not var_name.startswith('__'):
                # Check if this variable was read (not written)
                if f'read:{var_name}' in event.memory_access:
                    used_vars.add(var_name)
        
        return used_vars
    
    def _is_control_statement(self, event) -> bool:
        """Check if this event represents a control flow statement"""
        # This is simplified - would need source code analysis
        # For now, we check if it's a line event (not call/return)
        return event.event_type == 'line'
    
    def _extract_control_variables(self, event) -> Set[str]:
        """Extract variables used in control conditions"""
        control_vars = set()
        
        # Look for variables that were read (used in conditions)
        for access in event.memory_access:
            if access.startswith('read:'):
                var_name = access.split(':', 1)[1]
                control_vars.add(var_name)
        
        return control_vars
    
    def print_slice(self, slice_result: SliceResult, source_code: str = None):
        """
        Print the slice result in a readable format.
        
        Args:
            slice_result: Result from compute_dynamic_slice
            source_code: Optional source code to display
        """
        print("\n" + "="*80)
        print(f"DYNAMIC SLICE: {slice_result.target_var} @ Line {slice_result.target_line}")
        print("="*80)
        
        print(f"\nRelevant Lines: {sorted(slice_result.relevant_lines)}")
        
        if slice_result.data_dependencies:
            print("\nData Dependencies:")
            for line, deps in sorted(slice_result.data_dependencies.items()):
                print(f"  Line {line} depends on variables: {deps}")
        
        if slice_result.control_dependencies:
            print("\nControl Dependencies:")
            for line, deps in sorted(slice_result.control_dependencies.items()):
                print(f"  Line {line} controlled by lines: {deps}")
        
        if source_code:
            print("\nSliced Code:")
            lines = source_code.split('\n')
            for i, line in enumerate(lines, 1):
                if i in slice_result.relevant_lines:
                    print(f"  {i:3d} ✓ {line}")
                else:
                    print(f"  {i:3d}   {line}")
        
        print("\n" + "="*80 + "\n")


def slice_from_source(source_code: str, target_line: int, target_var: str):
    """
    Helper function to slice a program from source code.
    
    Args:
        source_code: Python source code as string
        target_line: Target line number
        target_var: Target variable name
        
    Returns:
        SliceResult
    """
    # This would require executing the code with tracer
    # For now, this is a placeholder for the main_runner integration
    from tracer_engine import Tracer
    
    # Compile and execute with tracer
    tracer = Tracer()
    
    # Execute the code
    exec_globals = {}
    tracer.start_trace()
    try:
        exec(source_code, exec_globals)
    finally:
        tracer.stop_trace()
    
    # Compute slice
    slicer = DynamicSlicer()
    slice_result = slicer.compute_dynamic_slice(
        tracer.get_trace_log(),
        target_line,
        target_var
    )
    
    return slice_result


# Example usage and testing
if __name__ == "__main__":
    from tracer_engine import Tracer
    
    # Test function with clear dependencies
    def test_function(x, y):
        a = x + 1      # Line 2
        b = y * 2      # Line 3
        c = a + b      # Line 4
        d = c * 2      # Line 5
        return d       # Line 6
    
    # Trace execution
    tracer = Tracer()
    result = tracer.trace_execution(test_function, 3, 4)
    
    print(f"Function result: {result}")
    
    # Compute slice for variable 'd' at line 5
    slicer = DynamicSlicer()
    slice_result = slicer.compute_dynamic_slice(
        tracer.get_trace_log(),
        target_line=5,
        target_var='d'
    )
    
    # Print slice
    source = """def test_function(x, y):
    a = x + 1      # Line 2
    b = y * 2      # Line 3
    c = a + b      # Line 4
    d = c * 2      # Line 5
    return d       # Line 6"""
    
    slicer.print_slice(slice_result, source)
    
    print("\nExpected: Lines affecting 'd' should include lines where a, b, c, x, y are defined")
