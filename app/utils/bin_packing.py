"""
Bin packing algorithm utilities
"""

from typing import List
from math import ceil
from ..models.listing import Listing
from ..models.vehicle_unit import VehicleUnit


def _round_up_to_10(value: int) -> int:
    return int(ceil(value / 10) * 10)


def _listing_capacity(listing: Listing) -> int:
    """Return the maximum linear capacity (in feet) a listing can provide
    to place vehicles of width 10 in a single row with consistent orientation.
    We can choose the orientation per listing.
    """
    cap_len = listing.length if listing.width >= 10 else 0
    cap_wid = listing.width if listing.length >= 10 else 0
    return max(cap_len, cap_wid)


def _price_per_capacity(listing: Listing) -> float:
    cap = max(_listing_capacity(listing), 1)
    return listing.price_in_cents / cap


class BinPackingAlgorithm:
    """Packing allowing multiple vehicles per listing (single row, no gaps)."""

    @staticmethod
    def can_fit_vehicles(vehicles: List[VehicleUnit], listings: List[Listing]) -> bool:
        return len(BinPackingAlgorithm.find_optimal_combination(vehicles, listings)) > 0

    @staticmethod
    def find_optimal_combination(vehicles: List[VehicleUnit], listings: List[Listing]) -> List[Listing]:
        if not vehicles or not listings:
            return []

        # Convert vehicles to sizes (rounded up to nearest 10)
        sizes = sorted([_round_up_to_10(v.length) for v in vehicles], reverse=True)

        # Prepare unused bins (listings) sorted by price per capacity (cheapest first)
        # Filter out listings that cannot fit even the smallest vehicle (width < 10 or capacity < 10)
        valid_listings = [l for l in listings if _listing_capacity(l) >= 10]
        if not valid_listings:
            return []

        unused = sorted(valid_listings, key=_price_per_capacity)

        # Open bins: list of tuples (listing, remaining_capacity)
        open_bins: List[tuple[Listing, int]] = []

        for s in sizes:
            # Try best-fit among open bins
            best_idx = -1
            best_leftover = None
            for idx, (lst, rem) in enumerate(open_bins):
                if rem >= s:
                    leftover = rem - s
                    if best_leftover is None or leftover < best_leftover:
                        best_leftover = leftover
                        best_idx = idx
            if best_idx != -1:
                # Place in best existing bin
                lst, rem = open_bins[best_idx]
                open_bins[best_idx] = (lst, rem - s)
                continue

            # Need to open a new bin: choose cheapest listing that can accommodate s
            chosen_idx = -1
            for idx, lst in enumerate(unused):
                if _listing_capacity(lst) >= s:
                    chosen_idx = idx
                    break
            if chosen_idx == -1:
                # No listing can fit this vehicle size
                return []
            lst = unused.pop(chosen_idx)
            cap = _listing_capacity(lst)
            open_bins.append((lst, cap - s))

        # Extract used listings in the order opened
        used_listings = [lst for (lst, _) in open_bins]
        return used_listings

    @staticmethod
    def calculate_total_price(listings: List[Listing]) -> int:
        return sum(listing.price_in_cents for listing in listings)