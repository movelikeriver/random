import java.util.ArrayList;
import java.util.Calendar;

import base.CpuTimer;
import base.Report;
import base.TaskManager;

public class VectorReallocation {

	public static class TestResult {
		public String resultOverall = new String();
		public String resultDetails = new String();
		public long totalCostInMs = -1;
	}

	public static void scheduleTasks(int num, ArrayList<Report> taskArr,
			TaskManager taskManager) {
		for (int i = 0; i < num; i++) {
			int index = taskArr.size();
			Report report = new Report();
			taskArr.add(report);
			// The reference pointing to the element.
			taskManager.addTask(taskArr.get(index));
		}
	}

	public static TestResult testScheduleTasks() {
		TestResult result = new TestResult();
		StringBuilder sb = new StringBuilder();
		sb.append("For ");
		sb.append(Report.TEST_MODE.toString());
		sb.append(", RECUR_N=");
		sb.append(Report.RECUR_N);
		sb.append(" and NUM_TASKS=");
		sb.append(Report.NUM_TASKS);
		sb.append("\n");
		result.resultOverall = sb.toString();

		ArrayList<Report> taskArr = new ArrayList<Report>();
		TaskManager taskManager = new TaskManager();
		VectorReallocation
				.scheduleTasks(Report.NUM_TASKS, taskArr, taskManager);

		sb.setLength(0);
		sb.append(Calendar.getInstance().getTime().toString());
		sb.append("  Before: ");
		result.resultDetails = result.resultDetails.concat(sb.toString());
		result.resultDetails = result.resultDetails.concat(VectorReallocation
				.printArr(taskArr));

		CpuTimer timer = new CpuTimer();
		timer.start();
		taskManager.run();
		timer.stop();

		sb.setLength(0);
		sb.append(Calendar.getInstance().getTime().toString());
		sb.append("  After: ");
		result.resultDetails = result.resultDetails.concat(sb.toString());
		result.resultDetails = result.resultDetails.concat(VectorReallocation
				.printArr(taskArr));

		sb.setLength(0);
		sb.append("RUN_IN_PARALLEL=");
		sb.append(Report.RUN_IN_PARALLEL);
		sb.append(", ");
		result.resultOverall = result.resultOverall.concat(sb.toString());

		sb.setLength(0);
		sb.append("total in ms: ");
		sb.append(timer.getInMs());
		sb.append("\n");
		result.totalCostInMs = timer.getInMs();
		result.resultOverall = result.resultOverall.concat(sb.toString());

		return result;
	}

	private static String printArr(final ArrayList<Report> taskArr) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < taskArr.size(); i++) {
			sb.append(Integer.toString(taskArr.get(i).cost));
			sb.append(", ");
		}
		sb.append("\n");
		return sb.toString();
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		ArrayList<TestResult> retArr = new ArrayList<TestResult>();
		{
			Report.TEST_MODE = Report.RunMode.FIBONACCI_RECUR;
			Report.RECUR_N = 40;
			{
				Report.RUN_IN_PARALLEL = false;
				TestResult ret = VectorReallocation.testScheduleTasks();
				retArr.add(ret);
				System.out.println(ret.resultDetails);
			}
			{
				Report.RUN_IN_PARALLEL = true;
				TestResult ret = VectorReallocation.testScheduleTasks();
				retArr.add(ret);
				System.out.println(ret.resultDetails);
			}
		}
		{
			Report.TEST_MODE = Report.RunMode.FIBONACCI_FAST;
			Report.RECUR_N = 90;
			{
				Report.RUN_IN_PARALLEL = false;
				TestResult ret = VectorReallocation.testScheduleTasks();
				retArr.add(ret);
				System.out.println(ret.resultDetails);
			}
			{
				Report.RUN_IN_PARALLEL = true;
				TestResult ret = VectorReallocation.testScheduleTasks();
				retArr.add(ret);
				System.out.println(ret.resultDetails);
			}
		}
		{
			Report.TEST_MODE = Report.RunMode.PRIME_NUM;
			{
				Report.RUN_IN_PARALLEL = false;
				TestResult ret = VectorReallocation.testScheduleTasks();
				retArr.add(ret);
				System.out.println(ret.resultDetails);
			}
			{
				Report.RUN_IN_PARALLEL = true;
				TestResult ret = VectorReallocation.testScheduleTasks();
				retArr.add(ret);
				System.out.println(ret.resultDetails);
			}
		}

		long costSequentially = 0;
		for (int i = 0; i < retArr.size(); i++) {
			TestResult result = retArr.get(i);
			if (i % 2 == 0) {
				// sequentially
				costSequentially = result.totalCostInMs;
			} else {
				// in parallel
				result.resultOverall = result.resultOverall.concat(String
						.format("%.4f x\n", (double) costSequentially
								/ (double) result.totalCostInMs));
			}
			System.out.println(result.resultDetails);
		}

		// Overall
		for (int i = 0; i < retArr.size(); i++) {
			System.out.println(retArr.get(i).resultOverall);
		}
	}

}
