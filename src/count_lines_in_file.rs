use memchr::memchr_iter;
use memmap2::MmapOptions;
use rayon::prelude::*;
use rayon::ThreadPoolBuilder;
// use std::env;
use std::fs::File;
use std::io;
// use std::time::Instant;

fn count_lines_simd(filename: &str, chunk_size: usize, num_threads: usize) -> io::Result<usize> {
    // Open the file.
    let file = File::open(filename)?;

    // Memory-map the file.
    let mmap = unsafe { MmapOptions::new().map(&file)? };

    // Create a local thread pool with the specified number of threads.
    let pool = ThreadPoolBuilder::new()
        .num_threads(num_threads)
        .build()
        .unwrap();

    // Use the local thread pool to execute the computation.
    let lines = pool.install(|| {
        mmap.par_chunks(chunk_size)
            .map(|chunk| memchr_iter(b'\n', chunk).count())
            .sum()
    });

    Ok(lines)
}

pub fn call(
    filename: &str,
    chunk_size: usize,
    num_threads: usize,
) -> Result<usize, std::io::Error> {
    let count = count_lines_simd(filename, chunk_size, num_threads)?;
    Ok(count)
}

// fn main() {
//     // Get command-line arguments.
//     let args: Vec<String> = env::args().collect();

//     if args.len() != 4 {
//         eprintln!(
//             "Usage: {} <filename> <chunk_size_in_bytes> <num_threads>",
//             args[0]
//         );
//         return;
//     }

//     let filename = &args[1];
//     let chunk_size: usize = args[2]
//         .parse()
//         .expect("Invalid chunk size (must be a positive integer)");
//     let num_threads: usize = args[3]
//         .parse()
//         .expect("Invalid number of threads (must be a positive integer)");

//     let start_time = Instant::now();

//     match count_lines_simd(filename, chunk_size, num_threads) {
//         Ok(lines) => {
//             let duration = start_time.elapsed();
//             println!("Total number of lines: {}", lines);
//             println!("Time taken: {:?}", duration);
//         }
//         Err(e) => {
//             eprintln!("Error: {}", e);
//         }
//     }
// }
