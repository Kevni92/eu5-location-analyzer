#!/usr/bin/env python3
"""Compatibility wrapper for the Economy pie injector.

EU5 1.3 writes the economy header widget name as an unquoted identifier
(`name = income_and_expenses`). 0.3.1-alpha accidentally searched only for
the quoted form. This wrapper installs a tolerant anchor matcher and then
runs the normal injector.
"""

from __future__ import annotations

import re

import add_economy_pies as pies


def find_scroll_list_anchor(text: str) -> re.Match[str]:
    header_pattern = re.compile(
        r'(?m)^[ \t]*name\s*=\s*"?income_and_expenses"?\s*$'
    )
    headers = list(header_pattern.finditer(text))
    if len(headers) != 1:
        raise SystemExit(
            "ERROR: Expected the Economy income/expense header marker once, "
            f"found {len(headers)}."
        )

    scroll_pattern = re.compile(
        r'(?m)^(?P<indent>[ \t]*)scroll_list\s*=\s*\{\s*$'
    )
    match = scroll_pattern.search(text, headers[0].end())
    if match is None:
        raise SystemExit(
            "ERROR: Could not find the Economy scroll_list after the income/expense header."
        )
    return match


pies.find_scroll_list_anchor = find_scroll_list_anchor
pies.main()
