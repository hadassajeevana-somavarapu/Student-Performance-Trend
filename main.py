# Student Performance Trend Analysis
# Compares scores across multiple exams, calculates improvements and declines,
# identifies consistently weak subjects, and classifies student performance.


def analyze_subject_trend(exam_names, scores):
    """
    exam_names: list of str, e.g., ['Exam 1', 'Exam 2', 'Exam 3']
    scores: list of float scores in chronological exam order
    """
    transitions = []
    total_improvement = 0.0
    total_decline = 0.0

    for idx in range(1, len(scores)):
        prev_score = scores[idx - 1]
        curr_score = scores[idx]
        delta = curr_score - prev_score

        if delta > 0:
            direction = "Improved"
            total_improvement += delta
        elif delta < 0:
            direction = "Declined"
            total_decline += abs(delta)
        else:
            direction = "Unchanged"

        transitions.append({
            "from_exam": exam_names[idx - 1],
            "to_exam": exam_names[idx],
            "delta": delta,
            "direction": direction,
        })

    net_change = scores[-1] - scores[0] if len(scores) >= 2 else 0.0
    avg_score = sum(scores) / len(scores) if scores else 0.0

    return {
        "scores": scores,
        "average": avg_score,
        "net_change": net_change,
        "total_improvement": total_improvement,
        "total_decline": total_decline,
        "transitions": transitions,
    }


def classify_student(overall_avg, net_overall_change, consistently_weak_count, weak_threshold):
    """
    Classifies a student using overall average score, net score trajectory,
    and count of consistently weak subjects.
    """
    if overall_avg < weak_threshold or consistently_weak_count >= 2:
        return "Needs Academic Intervention"
    if overall_avg >= 85.0 and net_overall_change >= 0 and consistently_weak_count == 0:
        return "Consistent High Achiever"
    if net_overall_change >= 5.0 and consistently_weak_count <= 1:
        return "Steady Improver"
    if overall_avg >= 60.0 and consistently_weak_count == 0:
        return "Satisfactory & Stable"
    return "Fluctuating / Watchlist"


def evaluate_student_performance(student_name, exam_names, subject_scores, weak_threshold=50.0):
    """
    subject_scores: dict mapping subject_name -> list of scores across exams
    """
    subject_trends = {}
    consistently_weak_subjects = []
    all_subject_averages = []
    first_exam_total = 0.0
    last_exam_total = 0.0
    subject_count = len(subject_scores)

    for subject, scores in subject_scores.items():
        clean_subject = subject.strip().title()
        trend = analyze_subject_trend(exam_names, scores)
        subject_trends[clean_subject] = trend
        all_subject_averages.append(trend["average"])

        if scores:
            first_exam_total += scores[0]
            last_exam_total += scores[-1]

        # A subject is consistently weak if every exam score is below weak_threshold
        if scores and all(s < weak_threshold for s in scores):
            consistently_weak_subjects.append(clean_subject)

    overall_avg = sum(all_subject_averages) / len(all_subject_averages) if all_subject_averages else 0.0
    avg_first = first_exam_total / subject_count if subject_count else 0.0
    avg_last = last_exam_total / subject_count if subject_count else 0.0
    net_overall_change = avg_last - avg_first

    classification = classify_student(
        overall_avg=overall_avg,
        net_overall_change=net_overall_change,
        consistently_weak_count=len(consistently_weak_subjects),
        weak_threshold=weak_threshold,
    )

    return {
        "student_name": student_name.strip().title(),
        "exam_names": exam_names,
        "weak_threshold": weak_threshold,
        "subject_trends": subject_trends,
        "consistently_weak_subjects": consistently_weak_subjects,
        "overall_avg": overall_avg,
        "net_overall_change": net_overall_change,
        "classification": classification,
    }


def print_trend_report(report):
    print("\n" + "=" * 76)
    print(f"STUDENT PERFORMANCE TREND REPORT: {report['student_name']}")
    print("=" * 76)
    print(f"Examinations Tracked : {', '.join(report['exam_names'])}")
    print(f"Weakness Threshold   : {report['weak_threshold']:.1f}")

    for subject, data in report["subject_trends"].items():
        scores_str = " -> ".join(f"{s:.1f}" for s in data["scores"])
        print(f"\nSubject: {subject}")
        print(f"  Scores ({scores_str}) | Avg: {data['average']:.2f} | Net Change: {data['net_change']:+.2f}")
        print(f"  Total Gains: +{data['total_improvement']:.2f} | Total Drops: -{data['total_decline']:.2f}")
        for t in data["transitions"]:
            print(f"    * {t['from_exam']} to {t['to_exam']}: {t['delta']:+.2f} ({t['direction']})")

    print("\n" + "-" * 76)
    if report["consistently_weak_subjects"]:
        print(f"Consistently Weak Subjects : {', '.join(report['consistently_weak_subjects'])}")
    else:
        print("Consistently Weak Subjects : None")

    print(f"Overall Average Score      : {report['overall_avg']:.2f}")
    print(f"Net Overall Avg Change     : {report['net_overall_change']:+.2f}")
    print(f"Student Classification       : {report['classification']}")
    print("=" * 76)


def main():
    student_name = input("Enter student name: ").strip()
    num_exams = int(input("Enter number of examinations: "))
    exam_names = []
    for i in range(1, num_exams + 1):
        name = input(f"  Enter name for Exam #{i} (e.g., Cycle Test 1): ").strip() or f"Exam {i}"
        exam_names.append(name)

    weak_threshold = float(input("\nEnter weakness threshold score (e.g., 50): "))
    num_subjects = int(input("Enter number of subjects: "))

    subject_scores = {}
    for i in range(1, num_subjects + 1):
        subj = input(f"\nEnter Subject #{i} name: ").strip()
        scores = []
        for exam in exam_names:
            score = float(input(f"  Score in {subj} for {exam}: "))
            scores.append(score)
        subject_scores[subj] = scores

    report = evaluate_student_performance(
        student_name=student_name,
        exam_names=exam_names,
        subject_scores=subject_scores,
        weak_threshold=weak_threshold,
    )
    print_trend_report(report)


if __name__ == "__main__":
    main()
