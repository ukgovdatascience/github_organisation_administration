from typing import Callable, Dict, List
import multiprocessing as mp


def parallelise_processing(callable_function: Callable, iterable: iter, cpu_count: int = mp.cpu_count(),
                           max_chunksize: int = 1000) -> List:
    """Parallelise processing of an iterable.

    Args:
        callable_function: A callable function that returns a dictionary.
        iterable: An iterable that will be split amongst the CPUs for parallel processing.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the processing.
        max_chunksize: Default: 1000. The maximum number of iterables per CPU.

    Returns:
        All the outputs of callable_function as a list.

    """

    # Calculate the number of chunks to be sent to each process; if this exceeds max_chunksize, set to max_chunksize
    chunk_size = len(iterable) / cpu_count
    chunk_size = min(int(chunk_size) + bool(chunk_size), max_chunksize)

    # Set up a `multiprocessing.Pool` object, and use it to get items for each iterable in parallel
    with mp.Pool(cpu_count) as pool:
        mp_items = list(pool.imap_unordered(callable_function, iterable, chunksize=chunk_size))

    # Return `mp_items`
    return mp_items


def parallelise_dictionary_processing(callable_function: Callable[..., Dict], iterable: iter,
                                      cpu_count: int = mp.cpu_count(), max_chunksize: int = 1000) -> Dict:
    """Parallelise processing of a dictionary.

    Args:
        callable_function: A callable function that returns a dictionary.
        iterable: An iterable that will be split amongst the CPUs for parallel processing.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the processing.
        max_chunksize: Default: 1000. The maximum number of iterables per CPU.

    Returns:
        All the outputs of callable_function collapsing into a single dictionary.

    """

    # Process the iterable in parallel
    mp_items = parallelise_processing(callable_function, iterable, cpu_count, max_chunksize)

    # Collapse the list of dictionaries in mp_items into a single dictionary - assumes there are no duplicate keys
    items = {k: v for d in mp_items for k, v in d.items()}

    # Assert that the above assumption is correct; if so return items
    assert len(items) == len(mp_items), "Iterable names are not unique!"
    return items
