import java.util.ArrayList;
import java.util.Calendar;

import base.CpuTimer;
import base.Report;
import base.TaskManager;

public class VectorReallocation {
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

	public static String testScheduleTasks() {
		String ret = new String();
		StringBuilder sb = new StringBuilder();			
		sb.append("For ");
		sb.append(Report.TEST_MODE.toString());
		sb.append(", RECUR_N=");
		sb.append(Report.RECUR_N);
		sb.append(" and NUM=TASKS=");
		sb.append(Report.NUM_TASKS);
		sb.append("\n");
		ret = sb.toString();

		ArrayList<Report> taskArr = new ArrayList<Report>();
		TaskManager taskManager = new TaskManager();
		VectorReallocation
				.scheduleTasks(Report.NUM_TASKS, taskArr, taskManager);

		sb.setLength(0);
		sb.append(Calendar.getInstance().getTime().toString());
		sb.append("  Before: ");
		ret = ret.concat(sb.toString());
		ret = ret.concat(VectorReallocation.printArr(taskArr));
		
		CpuTimer timer = new CpuTimer();
		timer.start();
		taskManager.run();
		timer.stop();

		sb.setLength(0);
		sb.append(Calendar.getInstance().getTime().toString());
		sb.append("  After: ");
		ret = ret.concat(sb.toString());
		ret = ret.concat(VectorReallocation.printArr(taskArr));

		sb.setLength(0);
		sb.append("RUN_IN_PARALLEL=");
		sb.append(Report.RUN_IN_PARALLEL);
		sb.append(", ");
		ret = ret.concat(sb.toString());

		sb.setLength(0);
		sb.append("total in ms: ");
		sb.append(timer.getInMs());
		ret = ret.concat(sb.toString());

		return ret;
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
		String str = VectorReallocation.testScheduleTasks();
		System.out.println(str);
	}

}
