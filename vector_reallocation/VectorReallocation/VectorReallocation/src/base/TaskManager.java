package base;

import java.util.ArrayList;
import java.util.List;

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
//		runSequentially();
		runInParallel();
	}

	public void runSequentially() {
		for (int i = 0; i < tasks.size(); i++) {
			tasks.get(i).run();
		}
	}

	public void runInParallel() {
		List<Thread> threads = new ArrayList<Thread>();
		for (int i = 0; i < tasks.size(); i++) {
			Thread worker = new Thread(tasks.get(i));
			worker.setName(String.valueOf(i));
			worker.start();
			threads.add(worker);
		}

		int running = 0;
		do {
			running = 0;
			for (Thread thread : threads) {
				if (thread.isAlive()) {
					running++;
				}
			}
		} while (running > 0);
	}
}