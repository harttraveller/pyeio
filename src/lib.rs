use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
mod count_lines_in_file;

#[pyfunction]
fn _test_function(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn _count_lines_in_file(
    py: Python<'_>,
    filename: String,
    chunk_size: usize,
    num_threads: usize,
) -> PyResult<PyObject> {
    // Return type changed to PyObject for conversion flexibility
    // Call the main function to count lines
    let count = count_lines_in_file::call(&filename, chunk_size, num_threads)?;
    // Convert count directly into a Python integer object
    Ok(count.into_py(py))
}

#[pymodule]
#[pyo3(name = "rs")]
fn pyeio(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_test_function, m)?)?;
    m.add_function(wrap_pyfunction!(_count_lines_in_file, m)?)?;
    Ok(())
}
