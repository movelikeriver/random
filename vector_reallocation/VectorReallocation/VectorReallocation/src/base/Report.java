package base;

import java.util.concurrent.CountDownLatch;

import base.CpuTimer;

public class Report implements Runnable {
	public int cost = -1;
	private CountDownLatch latch = null;

	// Don't try crazy num.
	// In 4-CPU Mac.
	// $ java -version
	// java version "1.7.0_67"
	// Java(TM) SE Runtime Environment (build 1.7.0_67-b01)
	// Java HotSpot(TM) 64-Bit Server VM (build 24.65-b04, mixed mode)
	//
	//
	// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9
	// RUN_IN_PARALLEL=false, total in ms: 12552
	//
	// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9
	// RUN_IN_PARALLEL=true, total in ms: 5583
	// 2.2483 x
	//
	// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9
	// RUN_IN_PARALLEL=false, total in ms: 212962
	//
	// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9
	// RUN_IN_PARALLEL=true, total in ms: 103223
	// 2.0631 x
	//
	// For PRIME_NUM, RECUR_N=90 and NUM_TASKS=9
	// RUN_IN_PARALLEL=false, total in ms: 520514
	//
	// For PRIME_NUM, RECUR_N=90 and NUM_TASKS=9
	// RUN_IN_PARALLEL=true, total in ms: 185111
	// 2.8119 x

	public static int RECUR_N = 40;
	public static int NUM_TASKS = 9;
	public static boolean RUN_IN_PARALLEL = true;

	public enum RunMode {
		FIBONACCI_RECUR, FIBONACCI_FAST, PRIME_NUM,
	};

	public static RunMode TEST_MODE = RunMode.FIBONACCI_RECUR;

	private static long MIN_PRIME_N = 100 * 1000;
	private static final long MAX_PRIME_N = 300 * 1000;

	private void update() {
		this.cost = insaneCompute();
	}

	private int insaneCompute() {
		CpuTimer timer = new CpuTimer();
		timer.start();
		switch (TEST_MODE) {
		case FIBONACCI_RECUR:
			fibonacciRecur(RECUR_N);
			break;
		case FIBONACCI_FAST:
			fibonacciFast(RECUR_N);
			break;
		case PRIME_NUM:
			primeNumTest();
			break;
		default:
			break;
		}
		timer.stop();
		int costMs = (int) timer.getInMs();
		System.out.println("cost_ms: " + costMs);
		return costMs;
	}

	private void primeNumTest() {
		System.out.println("Starting primeNumTest()...");
		for (long i = MIN_PRIME_N; i < MAX_PRIME_N; i++) {
			isTwoPrimeMultipleDummy(i);
		}
	}

	private boolean isTwoPrimeMultipleDummy(long num) {
		long n = num / 2;
		boolean found = false;
		for (long part1 = 2; part1 <= n; part1++) {
			if (num % part1 != 0) {
				continue;
			}
			long part2 = num / part1;
			if (part1 > part2) {
				break;
			}
			if (!isPrimeNumDummy(part1)) {
				continue;
			}
			if (!isPrimeNumDummy(part2)) {
				continue;
			}
			if (part1 > 500 && part2 > 500) {
				System.out.println("within " + MAX_PRIME_N + ", " + num + " = "
						+ part1 + " * " + part2);
			}
			found = true;
		}
		return found;
	}

	private boolean isPrimeNumDummy(long num) {
		long n = num / 2;
		for (int i = 2; i <= n; i++) {
			if (num % i == 0) {
				return false;
			}
		}
		return true;
	}

	private void fibonacciFast(int n) {
		System.out.println("Starting fibonacciFast(" + n + ")...");
		boolean verified = false;
		for (int round1 = 0; round1 < 10000; round1++) {
			for (int round2 = 0; round2 < 10000; round2++) {
				if (n <= 2) {
					return;
				}
				long a = 1;
				long b = 2;
				for (int i = 2; i < n; i++) {
					long c = a + b;
					a = b;
					b = c;
					if (b < 1) {
						System.out.println("WARNING  long overflow...");
					}
				}
				if (!verified) {
					System.out.println("Verify the value: " + b + ", "
							+ (double) a / (double) b);
					verified = true;
				}
			}
		}
	}

	private void fibonacciRecur(int n) {
		System.out.println("Starting fibonacciRecur(" + n + ")...");
		for (int i = 2; i < n; i++) {
			if (recur(i) < 1) {
				System.out.println("int overflow...");
			}
		}
		System.out.println("Verify the value: " + recur(n) + ", "
				+ (float) (recur(n - 1)) / (float) (recur(n)));

	}

	private int recur(int n) {
		if (n <= 2) {
			return n;
		}
		return recur(n - 1) + recur(n - 2);
	}

	public void setLatch(CountDownLatch latch) {
		this.latch = latch;
	}

	@Override
	public void run() {
		update();
		if (this.latch != null) {
			this.latch.countDown();
		}
	}
}
