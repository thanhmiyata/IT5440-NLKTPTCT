"""
Main Runner - Orchestrator for All Demos
=========================================
Entry point that demonstrates all 4 dynamic analysis techniques
and the Heisenbug challenge.
"""

import sys
from tracer_engine import Tracer
from execution_indexer import ExecutionIndexer, IndexedTracer
from dynamic_slicer import DynamicSlicer
from fault_localization import FaultLocalizer
from target_programs import (
    buggy_max, loop_example, factorial_buggy,
    generate_max_test_cases, generate_factorial_test_cases
)
from heisenbug_demo import demonstrate_heisenbug


def print_section_header(title: str):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def demo_1_tracing():
    """
    DEMO 1: Tracing
    Demonstrates lossless trace capture with sys.settrace
    """
    print_section_header("DEMO 1: TRACING - Lossless Execution Trace")
    
    print("Concept: Capture complete execution trace including:")
    print("  - Control Flow (line numbers)")
    print("  - Variable Values (local variables)")
    print("  - Memory Access (read/write operations)")
    print("\nTarget Function: loop_example(5)")
    print("-" * 80)
    
    # Create tracer
    tracer = Tracer()
    
    # Trace execution
    result = tracer.trace_execution(loop_example, 5)
    
    print(f"\nFunction Result: {result}")
    print(f"Total Trace Events: {len(tracer.get_trace_log())}")
    
    # Print trace (limited to first 25 events)
    tracer.print_trace(max_events=25)
    
    # Show variable history
    print("Variable 'result' History:")
    history = tracer.get_variable_history('result')
    for line, value in history[:10]:  # Show first 10
        print(f"  Line {line}: result = {value}")
    
    if len(history) > 10:
        print(f"  ... ({len(history) - 10} more)")
    
    return tracer


def demo_2_slicing(tracer: Tracer):
    """
    DEMO 2: Dynamic Slicing
    Demonstrates backward slicing to find dependencies
    """
    print_section_header("DEMO 2: DYNAMIC SLICING - Backward Dependency Analysis")
    
    print("Concept: Find all lines that affect a target variable")
    print("  - Data Dependencies (variables used in computation)")
    print("  - Control Dependencies (conditions affecting execution)")
    print("\nTarget: Variable 'result' at the end of loop_example")
    print("-" * 80)
    
    # Get trace from previous demo
    trace_log = tracer.get_trace_log()
    
    # Find the last line where 'result' appears
    target_line = None
    for event in reversed(trace_log):
        if 'result' in event.local_vars and event.event_type == 'line':
            target_line = event.line_number
            break
    
    if target_line is None:
        print("Could not find target variable in trace")
        return
    
    print(f"Target Line: {target_line}")
    print(f"Target Variable: result")
    
    # Compute slice
    slicer = DynamicSlicer()
    slice_result = slicer.compute_dynamic_slice(
        trace_log,
        target_line=target_line,
        target_var='result'
    )
    
    # Print results
    print(f"\nSlice Result:")
    print(f"  Relevant Lines: {sorted(slice_result.relevant_lines)}")
    print(f"  Total Lines in Slice: {len(slice_result.relevant_lines)}")
    
    if slice_result.data_dependencies:
        print(f"\n  Data Dependencies:")
        for line, deps in sorted(slice_result.data_dependencies.items())[:5]:
            print(f"    Line {line} depends on: {deps}")
    
    return slice_result


def demo_3_indexing():
    """
    DEMO 3: Execution Indexing
    Demonstrates unique execution point identification
    """
    print_section_header("DEMO 3: EXECUTION INDEXING - Unique Execution Points")
    
    print("Concept: Assign unique ID to each execution point")
    print("  Format: <Calling Context, Statement (Line), Instance>")
    print("  - Context: Function call stack")
    print("  - Statement: Line number")
    print("  - Instance: Iteration count for loops")
    print("\nTarget Function: loop_example(3)")
    print("-" * 80)
    
    # Create tracer and indexer
    tracer = Tracer()
    result = tracer.trace_execution(loop_example, 3)
    
    # Create indexed trace
    indexed_tracer = IndexedTracer()
    indexed_trace = indexed_tracer.trace_with_indexing(tracer.get_trace_log())
    
    print(f"\nFunction Result: {result}")
    print(f"Total Execution Points: {len(indexed_trace)}")
    
    # Print indexed trace
    indexed_tracer.print_indexed_trace(indexed_trace, max_events=20)
    
    # Show statistics
    stats = indexed_tracer.indexer.get_statistics()
    print("\nExecution Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nKey Insight: Notice how loop iterations have different Instance numbers")
    print("This allows us to distinguish between different executions of the same line")
    
    return indexed_tracer


def demo_4_fault_localization():
    """
    DEMO 4: Fault Localization
    Demonstrates spectrum-based fault localization with Tarantula
    """
    print_section_header("DEMO 4: FAULT LOCALIZATION - Finding Buggy Lines")
    
    print("Concept: Identify suspicious lines using test coverage")
    print("  - Run multiple test cases (some pass, some fail)")
    print("  - Build coverage matrix")
    print("  - Apply Tarantula formula to rank suspiciousness")
    print("\nTarget Function: buggy_max (has a bug in line 6)")
    print("-" * 80)
    
    # Create fault localizer
    localizer = FaultLocalizer()
    
    # Add test cases
    test_cases = generate_max_test_cases()
    for i, (inputs, expected) in enumerate(test_cases):
        localizer.add_test_case(
            name=f"test_{i+1}",
            input_args=inputs,
            expected_output=expected
        )
    
    print(f"Added {len(test_cases)} test cases")
    
    # Run tests
    print("Running tests with coverage tracking...")
    localizer.run_tests(buggy_max)
    
    # Print results
    localizer.print_results(top_n=10)
    
    # Get most suspicious line
    most_suspicious = localizer.get_most_suspicious_line()
    print(f"\n🎯 Most Suspicious Line: {most_suspicious}")
    print("   Expected: Line with 'max_val = b' instead of 'max_val = c'")
    
    return localizer


def demo_5_heisenbug():
    """
    DEMO 5: Heisenbug
    Demonstrates race condition that appears/disappears with perturbation
    """
    print_section_header("DEMO 5: HEISENBUG - Race Condition with Perturbation")
    
    print("Concept: A bug that changes behavior when observed")
    print("  - Race condition in multi-threaded bank transfer")
    print("  - Bug may hide in normal (fast) execution")
    print("  - Perturbation (delay injection) reveals the bug")
    print("  - Proper synchronization eliminates the bug")
    print("-" * 80)
    
    # Run the heisenbug demonstration
    demonstrate_heisenbug()


def run_all_demos():
    """Run all demonstrations in sequence"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  HOMEWORK 3: DYNAMIC PROGRAM ANALYSIS - COMPLETE DEMONSTRATION".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    print("\nThis demonstration covers 4 core concepts + 1 advanced challenge:")
    print("  1. Tracing - Lossless execution trace capture")
    print("  2. Dynamic Slicing - Backward dependency analysis")
    print("  3. Execution Indexing - Unique execution point identification")
    print("  4. Fault Localization - Spectrum-based bug finding")
    print("  5. Heisenbug - Race condition with perturbation")
    
    input("\nPress Enter to start the demonstrations...")
    
    # Demo 1: Tracing
    tracer = demo_1_tracing()
    input("\nPress Enter to continue to Demo 2 (Dynamic Slicing)...")
    
    # Demo 2: Slicing
    slice_result = demo_2_slicing(tracer)
    input("\nPress Enter to continue to Demo 3 (Execution Indexing)...")
    
    # Demo 3: Indexing
    indexed_tracer = demo_3_indexing()
    input("\nPress Enter to continue to Demo 4 (Fault Localization)...")
    
    # Demo 4: Fault Localization
    localizer = demo_4_fault_localization()
    input("\nPress Enter to continue to Demo 5 (Heisenbug)...")
    
    # Demo 5: Heisenbug
    demo_5_heisenbug()
    
    # Final summary
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    print("\nSummary:")
    print("  ✓ Demo 1: Traced execution and captured variable states")
    print("  ✓ Demo 2: Computed dynamic slice showing dependencies")
    print("  ✓ Demo 3: Indexed execution points with unique IDs")
    print("  ✓ Demo 4: Localized fault using Tarantula algorithm")
    print("  ✓ Demo 5: Demonstrated Heisenbug with race condition")
    
    print("\nFor more details, see README.md")
    print("="*80 + "\n")


def run_quick_demo():
    """Run a quick demo without pauses"""
    print("\n" + "="*80)
    print("QUICK DEMO MODE - All demonstrations without pauses")
    print("="*80)
    
    tracer = demo_1_tracing()
    slice_result = demo_2_slicing(tracer)
    indexed_tracer = demo_3_indexing()
    localizer = demo_4_fault_localization()
    demo_5_heisenbug()
    
    print("\n" + "="*80)
    print("QUICK DEMO COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    else:
        run_all_demos()
