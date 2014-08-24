import java.util.ArrayList;
import java.util.Calendar;

import base.CpuTimer;
import base.Report;
import base.TaskManager;

public class VectorReallocation {
	public void scheduleTasks(int num, ArrayList<Report> taskArr,
			TaskManager taskManager) {
		for (int i = 0; i < num; i++) {
			int index = taskArr.size();
			Report report = new Report();
			taskArr.add(report);
			// The reference pointing to the element.
			taskManager.addTask(taskArr.get(index));
		}
	}

	public void testScheduleTasks() {
		ArrayList<Report> taskArr = new ArrayList<Report>();
		TaskManager taskManager = new TaskManager();
		scheduleTasks(Report.NUM_TASKS, taskArr, taskManager);
		System.out.println(
				Calendar.getInstance().getTime().toString() +
				"  Before:");
		VectorReallocation.printArr(taskArr);
		
		CpuTimer timer = new CpuTimer();
		timer.start();
		taskManager.run();
		timer.stop();
		
		System.out.println(
				Calendar.getInstance().getTime().toString() +
				"  After:");
		VectorReallocation.printArr(taskArr);
		
		System.out.println("Total in ms: " + timer.getInMs());
	}
	
	private static void printArr(final ArrayList<Report> taskArr) {
		for (int i = 0; i < taskArr.size(); i++) {
			System.out.println(taskArr.get(i).cost);
		}
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		VectorReallocation vr = new VectorReallocation();
		vr.testScheduleTasks();
	}

}
