package base;

import java.util.Calendar;

public class Report implements Runnable {
	public int cost = -1;
	// Don't try crazy num.
	// In 4-CPU Mac, for RECUR_N=40 and NUM_TASKS=9:
	// 1283ms * 9 sequentially
	// 5887ms in parallel
	private static final int RECUR_N = 40;
	public static final int NUM_TASKS = 9;

	private void update() {
		this.cost = insaneCompute();
	}

	private int insaneCompute() {
		System.out.println("Start insaneCompute()...");
		long start = Calendar.getInstance().getTimeInMillis();
		for (int i = 2; i < RECUR_N; i++) {
			if (recur(i) < 1) {
				System.out.println("int overflow...");
			}
		}
		System.out.println("Verify the value: " + recur(RECUR_N) + ", "
				+ (float) (recur(RECUR_N - 1)) / (float) (recur(RECUR_N)));
		int costMs = (int) (Calendar.getInstance().getTimeInMillis() - start);
		System.out.println("cost_ms: " + costMs);
		return costMs;
	}

	private int recur(int n) {
		if (n <= 2) {
			return n;
		}
		return recur(n - 1) + recur(n - 2);
	}

	@Override
	public void run() {
		update();
	}
}
