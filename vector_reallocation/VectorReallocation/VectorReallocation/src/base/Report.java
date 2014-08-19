package base;

import java.util.Calendar;

public class Report implements Runnable {
	public int cost = -1;
	private static final int RECUR_N = 27;  // don't try crazy num.
	
	private void update() {
		this.cost = insaneCompute();
	}
	
	private int insaneCompute() {
		System.out.println("Start insaneCompute()...");
	    long start = Calendar.getInstance().getTimeInMillis();
		for (int i = 2; i < RECUR_N; i++) {
			recur(i);
		}
		int costMs = (int)(Calendar.getInstance().getTimeInMillis() - start);
		System.out.println("cost_ms: " + costMs);
		return costMs;
	}
	
	private int recur(int n) {
		if (n <= 2) {
			return n;
		}
		int sum = 0;
		for (int i = 0; i < n; i++) {
			sum += recur(i);
		}
		return sum;
	}

	@Override
	public void run() {
		update();	
	}
}
