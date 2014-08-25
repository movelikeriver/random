package base;

import java.util.ArrayList;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

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
		if (Report.RUN_IN_PARALLEL) {
			runInParallel();
		} else {
			runSequentially();
		}
	}

	public void runSequentially() {
		for (int i = 0; i < tasks.size(); i++) {
			tasks.get(i).run();
		}
	}

	public void runInParallel() {
	    CountDownLatch latch = new CountDownLatch(tasks.size());
	    ExecutorService executor = Executors.newFixedThreadPool(tasks.size()); 
		for (int i = 0; i < tasks.size(); i++) {
			Report task = tasks.get(i);
			task.setLatch(latch);
			executor.submit(task);
		}
		
		try {
			latch.await();
		} catch (InterruptedException e) {
	        e.printStackTrace();
	    }
	}
}