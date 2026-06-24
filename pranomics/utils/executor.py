from pranomics.utils.checkpoint import is_done, mark_done


def run_step(sample, step_name, function, *args, **kwargs):
    if is_done(sample, step_name):
        print(f"{step_name} already completed: {sample}")
        return None

    try:
        result = function(*args, **kwargs)
    except Exception as exc:
        print(f"{step_name} failed for {sample}: {exc}")
        raise

    mark_done(sample, step_name)
    print(f"{step_name} completed: {sample}")
    return result
