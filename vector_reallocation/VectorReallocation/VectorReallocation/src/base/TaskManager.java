package base;

import java.util.ArrayList;
import base.Report;

public class TaskManager {
	private ArrayList<Report> tasks = null;

	public TaskManager() {
		this.tasks = new ArrayList<Report>();
	}

	public void addTask(Report report) {
		tasks.add(report);
	}

	public void run() {
		for (int i = 0; i < tasks.size(); i++) {
			update(tasks.get(i));
		}
	}

	private void update(Report report) {
		report.cost = 10;
	}
}