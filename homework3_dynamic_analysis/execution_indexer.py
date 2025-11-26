"""
Execution Indexer - Concept 3: Execution Indexing
==================================================
Implements execution indexing to assign unique IDs to execution points.
Uses the tuple: <Calling Context, Statement (Line), Instance>
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ExecutionPoint:
    """Represents a unique execution point in the program"""
    context: Tuple[str, ...]  # Calling context (stack of function names)
    statement: int  # Line number
    instance: int  # Instance number (for loops/repeated executions)
    
    def __hash__(self):
        return hash((self.context, self.statement, self.instance))
    
    def __eq__(self, other):
        if not isinstance(other, ExecutionPoint):
            return False
        return (self.context == other.context and 
                self.statement == other.statement and 
                self.instance == other.instance)
    
    def __repr__(self):
        context_str = "->".join(self.context) if self.context else "main"
        return f"<{context_str}, L{self.statement}, #{self.instance}>"


class ExecutionIndexer:
    """
    Execution Indexer that assigns unique IDs to execution points.
    
    Key concepts:
    - Context: Stack of function calls (calling context)
    - Statement: Line number being executed
    - Instance: How many times this line has been executed in this context
    """
    
    def __init__(self):
        self.context_stack: List[str] = []  # Stack of function names
        # Key: (context_tuple, line_number), Value: instance count
        self.instance_counters: Dict[Tuple[Tuple[str, ...], int], int] = defaultdict(int)
        self.execution_points: List[ExecutionPoint] = []
        self.current_index = 0
        
    def push_context(self, function_name: str):
        """
        Push a function onto the calling context stack.
        Called when entering a function.
        
        Args:
            function_name: Name of the function being entered
        """
        self.context_stack.append(function_name)
    
    def pop_context(self):
        """
        Pop a function from the calling context stack.
        Called when exiting a function.
        """
        if self.context_stack:
            self.context_stack.pop()
    
    def get_current_context(self) -> Tuple[str, ...]:
        """Get the current calling context as a tuple"""
        return tuple(self.context_stack)
    
    def record_execution(self, line_number: int, function_name: str = None) -> ExecutionPoint:
        """
        Record an execution point and assign it a unique ID.
        
        Args:
            line_number: Line number being executed
            function_name: Optional function name (for context management)
            
        Returns:
            ExecutionPoint with unique ID
        """
        # Get current context
        context = self.get_current_context()
        
        # Create key for instance counter
        counter_key = (context, line_number)
        
        # Increment instance counter for this context+line combination
        self.instance_counters[counter_key] += 1
        instance = self.instance_counters[counter_key]
        
        # Create execution point
        exec_point = ExecutionPoint(
            context=context,
            statement=line_number,
            instance=instance
        )
        
        self.execution_points.append(exec_point)
        self.current_index += 1
        
        return exec_point
    
    def reset(self):
        """Reset the indexer state"""
        self.context_stack = []
        self.instance_counters.clear()
        self.execution_points = []
        self.current_index = 0
    
    def compare_points(self, point1: ExecutionPoint, point2: ExecutionPoint) -> bool:
        """
        Compare two execution points to see if they represent the same location.
        
        Args:
            point1: First execution point
            point2: Second execution point
            
        Returns:
            True if points are identical
        """
        return point1 == point2
    
    def find_matching_points(self, target_point: ExecutionPoint) -> List[int]:
        """
        Find all indices of execution points that match the target.
        
        Args:
            target_point: Execution point to search for
            
        Returns:
            List of indices where matching points were found
        """
        matching_indices = []
        for i, point in enumerate(self.execution_points):
            if self.compare_points(point, target_point):
                matching_indices.append(i)
        return matching_indices
    
    def get_execution_point(self, index: int) -> Optional[ExecutionPoint]:
        """Get execution point at a specific index"""
        if 0 <= index < len(self.execution_points):
            return self.execution_points[index]
        return None
    
    def print_execution_index(self, max_points: int = 30):
        """
        Print the execution index in a readable format.
        
        Args:
            max_points: Maximum number of points to print
        """
        print("\n" + "="*80)
        print("EXECUTION INDEX")
        print("="*80)
        
        for i, point in enumerate(self.execution_points[:max_points]):
            print(f"[{i:3d}] {point}")
        
        if len(self.execution_points) > max_points:
            print(f"\n... ({len(self.execution_points) - max_points} more points)")
        
        print("\n" + "="*80)
        print(f"Total Execution Points: {len(self.execution_points)}")
        print("="*80 + "\n")
    
    def get_statistics(self) -> Dict[str, any]:
        """Get statistics about the execution"""
        stats = {
            'total_points': len(self.execution_points),
            'unique_contexts': len(set(point.context for point in self.execution_points)),
            'unique_statements': len(set(point.statement for point in self.execution_points)),
            'max_instance': max((point.instance for point in self.execution_points), default=0),
            'context_depth': len(self.context_stack)
        }
        return stats


class IndexedTracer:
    """
    Combines Tracer functionality with Execution Indexing.
    Wraps around the basic tracer to add indexing capabilities.
    """
    
    def __init__(self):
        self.indexer = ExecutionIndexer()
        self.trace_to_index_map: Dict[int, ExecutionPoint] = {}
        
    def trace_with_indexing(self, trace_log: List) -> List[Tuple[any, ExecutionPoint]]:
        """
        Add execution indexing to a trace log.
        
        Args:
            trace_log: List of trace events from Tracer
            
        Returns:
            List of (trace_event, execution_point) tuples
        """
        self.indexer.reset()
        indexed_trace = []
        
        for trace_event in trace_log:
            # Handle context changes
            if trace_event.event_type == 'call':
                self.indexer.push_context(trace_event.function_name)
            elif trace_event.event_type == 'return':
                self.indexer.pop_context()
            
            # Record execution point
            exec_point = self.indexer.record_execution(
                line_number=trace_event.line_number,
                function_name=trace_event.function_name
            )
            
            indexed_trace.append((trace_event, exec_point))
        
        return indexed_trace
    
    def print_indexed_trace(self, indexed_trace: List[Tuple], max_events: int = 20):
        """Print trace with execution indices"""
        print("\n" + "="*80)
        print("INDEXED EXECUTION TRACE")
        print("="*80)
        
        for i, (trace_event, exec_point) in enumerate(indexed_trace[:max_events]):
            print(f"\n[{i:3d}] {exec_point}")
            print(f"      Event: {trace_event.event_type} at line {trace_event.line_number}")
            print(f"      Function: {trace_event.function_name}")
        
        if len(indexed_trace) > max_events:
            print(f"\n... ({len(indexed_trace) - max_events} more events)")
        
        print("\n" + "="*80)


# Example usage and testing
if __name__ == "__main__":
    # Test with a simple loop
    def loop_example(n):
        result = 0
        for i in range(n):
            result += i
        return result
    
    # Simulate execution indexing
    indexer = ExecutionIndexer()
    
    print("Simulating execution of loop_example(3):")
    print("-" * 40)
    
    # Simulate function call
    indexer.push_context("loop_example")
    
    # Line 2: result = 0
    point1 = indexer.record_execution(2)
    print(f"Line 2 (result = 0): {point1}")
    
    # Line 3: for i in range(n) - executed 3 times
    for iteration in range(3):
        point = indexer.record_execution(3)
        print(f"Line 3 (for loop, iteration {iteration}): {point}")
        
        # Line 4: result += i
        point = indexer.record_execution(4)
        print(f"Line 4 (result += i, iteration {iteration}): {point}")
    
    # Line 5: return result
    point_return = indexer.record_execution(5)
    print(f"Line 5 (return): {point_return}")
    
    indexer.pop_context()
    
    # Print full index
    indexer.print_execution_index()
    
    # Print statistics
    stats = indexer.get_statistics()
    print("\nExecution Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
