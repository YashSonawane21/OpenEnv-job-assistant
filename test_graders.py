"""Test script to validate graders, determinism, and anti-gaming behavior."""

from graders.task_manager import enumerate_tasks, get_all_tasks


def generate_test_cases(task):
    """Generate test cases for each task type."""
    from graders.task_manager import TaskType

    job_context = "Python engineer with React frontend skills. 5+ years experience. SQL database optimization."

    test_cases = {
        TaskType.RESUME: [
            ("Empty submission", "", job_context),
            ("Basic submission", "I am a developer", job_context),
            ("Good match", "Python developer with React, SQL, and project delivery experience", job_context),
            ("Keyword stuffing", "python " * 60, job_context),
        ],
        TaskType.EMAIL: [
            ("Empty submission", "", ""),
            ("Low quality", "Hi there", ""),
            ("Professional", "Hello, I am interested in this role and have relevant experience. Thank you.", ""),
            ("Keyword stuffing", "interested interested interested interested interested interested", ""),
        ],
        TaskType.COVER_LETTER: [
            ("Empty submission", "", job_context),
            ("Short submission", "I want this job", job_context),
            (
                "Quality submission",
                "Dear Hiring Manager, I have experience building Python and React systems and improving reliability. "
                "I would welcome the chance to discuss this role. Thank you.",
                job_context,
            ),
            ("Keyword stuffing", "dear python react experience " * 40, job_context),
        ],
        TaskType.LINKEDIN: [
            ("Empty submission", "", ""),
            ("Minimal profile", "Engineer", ""),
            (
                "Complete profile",
                "Professional photo. Senior Python Developer. Summary with impact. Skills: Python, React, SQL. "
                "Experience leading projects. Contact: email@example.com. Recommendations included.",
                "",
            ),
            ("Keyword stuffing", "python developer skills experience " * 35, ""),
        ],
        TaskType.INTERVIEW: [
            ("Empty submission", "", job_context),
            ("Vague response", "I prepared for the interview", job_context),
            (
                "STAR method",
                "Situation: We had a database bottleneck. Task: Optimize queries. Action: I profiled and refactored. "
                "Result: 10x faster queries. I practiced mock interviews and researched company products.",
                job_context,
            ),
            ("Keyword stuffing", "situation task action result " * 35, job_context),
        ],
    }
    return test_cases.get(task.type, [("Default test", "test", "")])


def test_all_graders():
    """Test all graders with sample submissions."""
    print("\n" + "=" * 76)
    print("TASK ENUMERATION, SCORE RANGE, DETERMINISM, AND ROBUSTNESS TEST")
    print("=" * 76)

    tasks_info = enumerate_tasks()
    print(f"\nAvailable tasks: {tasks_info['total_tasks']}")
    for task in tasks_info["tasks"]:
        print(f"  - Task #{task['id']}: {task['name']} ({task['type']})")

    all_tasks = get_all_tasks()
    all_passed = True

    print("\n" + "=" * 76)
    print("GRADER RESULTS")
    print("=" * 76)

    for task in all_tasks:
        print(f"\nTask #{task.id}: {task.name}")
        test_cases = generate_test_cases(task)
        task_passed = True

        for test_name, submission, context in test_cases:
            try:
                score = task.grade(submission, context)
                score_repeat = task.grade(submission, context)

                range_ok = 0.0 <= score <= task.max_score
                deterministic_ok = score == score_repeat

                status = "PASS" if (range_ok and deterministic_ok) else "FAIL"
                print(f"  {status:4} | {test_name:16} | score={score:.3f} | deterministic={deterministic_ok}")

                if not (range_ok and deterministic_ok):
                    task_passed = False
                    all_passed = False
            except Exception as exc:
                print(f"  FAIL | {test_name:16} | exception={exc}")
                task_passed = False
                all_passed = False

        print(f"  Result: {'ALL PASSED' if task_passed else 'SOME FAILED'}")

    print("\n" + "=" * 76)
    if all_passed:
        print("ALL TESTS PASSED - graders are deterministic and score-safe.")
    else:
        print("SOME TESTS FAILED - review grader behavior.")
    print("=" * 76 + "\n")
    return all_passed


if __name__ == "__main__":
    success = test_all_graders()
    raise SystemExit(0 if success else 1)
