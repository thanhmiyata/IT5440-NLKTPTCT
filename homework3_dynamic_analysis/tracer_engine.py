"""
Tracer Engine - Concept 1: Tracing
====================================
Implements a lossless trace using sys.settrace to capture:
- Control Flow (line numbers executed)
- Variable Values (local variables at each step)
- Memory Access (simulated read/write operations)
"""

import sys
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class TraceEvent:
    """Represents a single event in the execution trace"""
    event_type: str  # 'line', 'call', 'return', 'exception'
    filename: str
    line_number: int
    function_name: str
    local_vars: Dict[str, Any] = field(default_factory=dict)
    memory_access: List[str] = field(default_factory=list)  # ['read:x', 'write:y']
    
    def __repr__(self):
        return (f"TraceEvent(type={self.event_type}, "
                f"line={self.line_number}, "
                f"func={self.function_name}, "
                f"vars={list(self.local_vars.keys())})")


class Tracer:
    """
    Main Tracer class using sys.settrace for dynamic analysis.
    
    Captures a complete execution trace including:
    - All lines executed (control flow)
    - Variable values at each step
    - Memory read/write operations
    """
    
    def __init__(self, target_function: Optional[Callable] = None):
        self.trace_log: List[TraceEvent] = []
        self.target_function = target_function
        self.previous_locals: Dict[str, Any] = {}
        self.is_tracing = False
        
    def trace_function(self, frame, event, arg):
        """
        Trace function called by sys.settrace.
        
        Args:
            frame: Current stack frame
            event: Event type ('call', 'line', 'return', 'exception')
            arg: Event-specific argument
        """
        if not self.is_tracing:
            return None
            
        # Get frame information
        filename = frame.f_code.co_filename
        line_number = frame.f_lineno
        function_name = frame.f_code.co_name
        
        # Skip tracing of the tracer itself and system files
        if 'tracer_engine' in filename or '<' in filename:
            return self.trace_function
            
        # Capture local variables (deep copy to avoid reference issues)
        current_locals = {}
        for var_name, var_value in frame.f_locals.items():
            try:
                current_locals[var_name] = deepcopy(var_value)
            except:
                # Some objects can't be deep copied, use repr instead
                current_locals[var_name] = repr(var_value)
        
        # Detect memory access (read/write operations)
        memory_access = self._detect_memory_access(current_locals)
        
        # Create trace event
        trace_event = TraceEvent(
            event_type=event,
            filename=filename,
            line_number=line_number,
            function_name=function_name,
            local_vars=current_locals,
            memory_access=memory_access
        )
        
        self.trace_log.append(trace_event)
        
        # Update previous locals for next comparison
        self.previous_locals = current_locals
        
        return self.trace_function
    
    def _detect_memory_access(self, current_locals: Dict[str, Any]) -> List[str]:
        """
        Detect memory read/write operations by comparing with previous state.
        
        Returns:
            List of memory access operations like ['write:x', 'read:y']
        """
        access_log = []
        
        # Detect writes (new variables or changed values)
        for var_name, var_value in current_locals.items():
            if var_name not in self.previous_locals:
                access_log.append(f"write:{var_name}")
            elif self.previous_locals.get(var_name) != var_value:
                access_log.append(f"write:{var_name}")
        
        # Detect reads (variables that existed but weren't modified)
        for var_name in self.previous_locals:
            if var_name in current_locals:
                if self.previous_locals[var_name] == current_locals.get(var_name):
                    access_log.append(f"read:{var_name}")
        
        return access_log
    
    def start_trace(self):
        """Start tracing execution"""
        self.is_tracing = True
        self.trace_log = []
        self.previous_locals = {}
        sys.settrace(self.trace_function)
    
    def stop_trace(self):
        """Stop tracing execution"""
        self.is_tracing = False
        sys.settrace(None)
    
    def trace_execution(self, func: Callable, *args, **kwargs):
        """
        Trace the execution of a function.
        
        Args:
            func: Function to trace
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function execution
        """
        self.start_trace()
        try:
            result = func(*args, **kwargs)
        finally:
            self.stop_trace()
        return result
    
    def get_trace_log(self) -> List[TraceEvent]:
        """Get the complete trace log"""
        return self.trace_log
    
    def print_trace(self, max_events: int = 50):
        """
        Print the trace log in a readable format.
        
        Args:
            max_events: Maximum number of events to print
        """
        print("\n" + "="*80)
        print("EXECUTION TRACE LOG")
        print("="*80)
        
        for i, event in enumerate(self.trace_log[:max_events]):
            print(f"\n[Event {i+1}] {event.event_type.upper()} at line {event.line_number}")
            print(f"  Function: {event.function_name}")
            print(f"  File: {event.filename}")
            
            if event.local_vars:
                print(f"  Local Variables:")
                for var_name, var_value in event.local_vars.items():
                    if not var_name.startswith('__'):  # Skip magic variables
                        print(f"    {var_name} = {var_value}")
            
            if event.memory_access:
                print(f"  Memory Access: {', '.join(event.memory_access)}")
        
        if len(self.trace_log) > max_events:
            print(f"\n... ({len(self.trace_log) - max_events} more events)")
        
        print("\n" + "="*80)
        print(f"Total Events: {len(self.trace_log)}")
        print("="*80 + "\n")
    
    def get_executed_lines(self) -> List[int]:
        """Get list of all line numbers that were executed"""
        return [event.line_number for event in self.trace_log if event.event_type == 'line']
    
    def get_variable_history(self, var_name: str) -> List[tuple]:
        """
        Get the history of a variable's values throughout execution.
        
        Args:
            var_name: Name of the variable to track
            
        Returns:
            List of (line_number, value) tuples
        """
        history = []
        for event in self.trace_log:
            if var_name in event.local_vars:
                history.append((event.line_number, event.local_vars[var_name]))
        return history


# Example usage and testing
if __name__ == "__main__":
    # Simple test function
    def test_function(n):
        result = 0
        for i in range(n):
            result += i
        return result
    
    # Create tracer and trace execution
    tracer = Tracer()
    output = tracer.trace_execution(test_function, 5)
    
    print(f"Function output: {output}")
    tracer.print_trace(max_events=20)
    
    # Show variable history
    print("\nVariable 'result' history:")
    for line, value in tracer.get_variable_history('result'):
        print(f"  Line {line}: result = {value}")
