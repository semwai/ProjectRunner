from typing import Literal


def colored(text: str, color: Literal["HEADER", "OKBLUE", "OKCYAN", "OKGREEN", "WARNING", "FAIL", "ENDC", "BOLD", "UNDERLINE"]) -> str:  # noqa
    pre = ""
    match color:
        case "HEADER":
            pre = '\033[95m'
        case "OKBLUE":
            pre = '\033[94m'
        case "OKCYAN":
            pre = '\033[96m'
        case "OKGREEN":
            pre = '\033[92m'
        case "WARNING":
            pre = '\033[93m'
        case "FAIL":
            pre = '\033[91m'
        case "ENDC":
            pre = '\033[0m'
        case "BOLD":
            pre = '\033[1m'
        case "UNDERLINE":
            pre = '\033[4m'
    return f"{pre}{text}\033[0m"

