"""
Test script to verify all graders work and scores are in valid range (0.0-1.0)
"""

from graders.task_manager import get_all_tasks, enumerate_tasks


def test_all_graders():
    """Test all graders with sample submissions."""
    
    print("\n" + "="*70)
    print("🧪 TASK ENUMERATION & GRADER VALIDATION TEST")
    print("="*70)
    
    # 1. Enumerate all tasks
    print("\n📋 AVAILABLE TASKS:")
    print("-" * 70)
    tasks_info = enumerate_tasks()
    for task in tasks_info["tasks"]:
        print(f"  Task #{task['id']}: {task['name']}")
        print(f"    Type: {task['type']} | Max Score: {task['max_score']}")
        print(f"    {task['description']}\n")
    
    # 2. Test each grader
    print("\n" + "="*70)
    print("🎯 GRADER TEST RESULTS")
    print("="*70)
    
    all_tasks = get_all_tasks()
    all_passed = True
    
    for task in all_tasks:
        print(f"\n✅ Task #{task.id}: {task.name}")
        print(f"   Grader: {task.grader.__module__}.{task.grader.__name__}")
        
        # Generate test submissions based on task type
        test_cases = generate_test_cases(task)
        
        task_passed = True
        for test_name, submission, context in test_cases:
            try:
                score = task.grade(submission, context)
                
                # Validate score range
                if 0.0 <= score <= task.max_score:
                    status = "✓ PASS"
                else:
                    status = "✗ FAIL (out of range)"
                    task_passed = False
                    all_passed = False
                
                print(f"   {status} | {test_name}: {score:.2f}")
            except Exception as e:
                print(f"   ✗ FAIL | {test_name}: {str(e)}")
                task_passed = False
                all_passed = False
        
        print(f"   Result: {'✅ ALL PASSED' if task_passed else '❌ SOME FAILED'}")
    
    # Summary
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - All graders return scores in 0.0-1.0 range")
    else:
        print("❌ SOME TESTS FAILED - Review graders for issues")
    print("="*70 + "\n")
    
    return all_passed


def generate_test_cases(task):
    """Generate test cases for each task type."""
    from graders.task_manager import TaskType
    
    job_context = "Python engineer with React frontend skills. 5+ years experience. SQL database optimization."
    
    test_cases = {
        TaskType.RESUME: [
            ("Empty submission", "", job_context),
            ("Basic submission", "I am a developer", job_context),
            ("Good match", "Python developer with React expertise and 6 years SQL experience", job_context),
        ],
        TaskType.EMAIL: [
            ("Empty submission", "", ""),
            ("Low quality", "Hi there", ""),
            ("Professional", "Hello, I am very interested in this position. Thank you for considering me.", ""),
        ],
        TaskType.COVER_LETTER: [
            ("Empty submission", "", job_context),
            ("Short submission", "I want this job", job_context),
            ("Quality submission", "Dear Hiring Manager, I have extensive experience in Python and React development. Looking forward to discussing this opportunity. Thank you", job_context),
        ],
        TaskType.LINKEDIN: [
            ("Empty submission", "", ""),
            ("Minimal profile", "Engineer", ""),
            ("Complete profile", "Senior Python Developer | 5+ years experience | Skills: Python, React, SQL, AWS | Photo | Contact: email@example.com", ""),
        ],
        TaskType.INTERVIEW: [
            ("Empty submission", "", job_context),
            ("Vague response", "I prepared for the interview", job_context),
            ("STAR method", "Situation: We had a database bottleneck. Task: Optimize queries. Action: I analyzed and refactored. Result: 10x faster queries. Studied company mission.", job_context),
        ],
    }
    
    return test_cases.get(task.type, [("Default test", "test", "")])


if __name__ == "__main__":
    success = test_all_graders()
    exit(0 if success else 1)
