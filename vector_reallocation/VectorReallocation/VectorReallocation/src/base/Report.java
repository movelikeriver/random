package base;

import java.util.Calendar;

public class Report implements Runnable {
	public int cost = -1;
	// Don't try crazy num.
	// In 4-CPU Mac.
	// $ java -version
	// java version "1.7.0_67"
	// Java(TM) SE Runtime Environment (build 1.7.0_67-b01)
	// Java HotSpot(TM) 64-Bit Server VM (build 24.65-b04, mixed mode)
	//
	// For FIBONACCI_RECUR, RECUR_N=40 and NUM_TASKS=9:
	// 1283 ms * 9 sequentially, 1.9614 x
	// 5887 ms in parallel
	//
	// For FIBONACCI_FAST, RECUR_N=90 and NUM_TASKS=9:
	// 20413 ms * 9 sequentially,  ??
	// 217103 ms in parallel,  ??
	//
	// For PRIME_NUM:
	// 49654 ms * 9 sequentially, 2.0662 x
	// 216279 ms in parallel

	private static final int RECUR_N = 90;
	public static final int NUM_TASKS = 9;
	public static final boolean RUN_IN_PARALLEL = false;

	private enum RunMode {
		FIBONACCI_RECUR, FIBONACCI_FAST, PRIME_NUM,
	};
	private static final RunMode TEST_MODE = RunMode.FIBONACCI_FAST;

	private static final long MIN_PRIME_N = 100 * 1000;
	private static final long MAX_PRIME_N = 300 * 1000;

	private void update() {
		this.cost = insaneCompute();
	}

	private int insaneCompute() {
		long start = Calendar.getInstance().getTimeInMillis();
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
		int costMs = (int) (Calendar.getInstance().getTimeInMillis() - start);
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

	@Override
	public void run() {
		update();
	}
}
