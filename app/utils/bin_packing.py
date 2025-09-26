"""
Bin packing algorithm utilities (2D lanes packing)
"""

from typing import List, Tuple, Optional
from math import ceil
from ..models.listing import Listing
from ..models.vehicle_unit import VehicleUnit


def _round_up_to_10(value: int) -> int:
    return int(ceil(value / 10) * 10)


def _orientations(listing: Listing) -> List[Tuple[int, int]]:
    """
    Return possible orientations for a listing as tuples (length_limit, lanes).
    lanes = floor(other_dimension / 10). Only lanes >= 1 are valid.
    """
    orientations: List[Tuple[int, int]] = []
    # Vehicle width fixed at 10. If we align vehicle length along listing.length,
    # the number of lanes is floor(listing.width/10)
    lanes1 = listing.width // 10
    if lanes1 >= 1:
        orientations.append((listing.length, lanes1))
    lanes2 = listing.length // 10
    if lanes2 >= 1:
        orientations.append((listing.width, lanes2))
    return orientations


def _best_orientation_for_length(listing: Listing, vehicle_length: int) -> Optional[Tuple[int, int]]:
    """Choose the orientation that can fit the given vehicle length and yields
    the most lanes. Return (length_limit, lanes), or None if not feasible.
    """
    candidates = [(L, lanes) for (L, lanes) in _orientations(listing) if L >= vehicle_length]
    if not candidates:
        return None
    # Prefer the one with more lanes (more capacity). Tie-breaker: larger length limit.
    candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return candidates[0]


def _price_per_lane(listing: Listing, vehicle_length: int) -> Optional[float]:
    ori = _best_orientation_for_length(listing, vehicle_length)
    if not ori:
        return None
    _, lanes = ori
    return listing.price_in_cents / lanes if lanes > 0 else None


class BinPackingAlgorithm:
    """Packing allowing multiple vehicles per listing using lanes (width/10) with same orientation.
    Each listing, once opened, fixes an orientation: a length_limit and a number of lanes.
    Vehicles are placed one per lane; lanes count down. No stacking along length.
    """

    @staticmethod
    def can_fit_vehicles(vehicles: List[VehicleUnit], listings: List[Listing]) -> bool:
        return len(BinPackingAlgorithm.find_optimal_combination(vehicles, listings)) > 0

    @staticmethod
    def find_optimal_combination(vehicles: List[VehicleUnit], listings: List[Listing]) -> List[Listing]:
        if not vehicles or not listings:
            return []

        # Convert vehicles to sizes (rounded up to nearest 10)
        sizes = sorted([_round_up_to_10(v.length) for v in vehicles], reverse=True)

        # Filter listings that can host at least one lane
        feasible_listings = [l for l in listings if (l.width // 10) >= 1 or (l.length // 10) >= 1]
        if not feasible_listings:
            return []

        # Open bins: list of (listing, length_limit, remaining_lanes)
        open_bins: List[Tuple[Listing, int, int]] = []
        # Track unused listings
        unused = feasible_listings.copy()

        for s in sizes:
            # Try place into existing bin with sufficient length_limit and lanes
            best_idx = -1
            best_lanes_left = -1
            for idx, (lst, Llim, lanes_left) in enumerate(open_bins):
                if lanes_left > 0 and Llim >= s:
                    if lanes_left > best_lanes_left:
                        best_lanes_left = lanes_left
                        best_idx = idx
            if best_idx != -1:
                lst, Llim, lanes_left = open_bins[best_idx]
                open_bins[best_idx] = (lst, Llim, lanes_left - 1)
                continue

            # Need to open a new bin: choose cheapest per-lane listing that can fit 's'
            # Compute price per lane for all unused that can fit
            candidates: List[Tuple[float, Listing, int, int]] = []  # (price_per_lane, listing, length_limit, lanes)
            for lst in unused:
                ori = _best_orientation_for_length(lst, s)
                if ori:
                    Llim, lanes = ori
                    ppl = lst.price_in_cents / lanes
                    candidates.append((ppl, lst, Llim, lanes))
            if not candidates:
                return []
            candidates.sort(key=lambda x: (x[0], -x[3], -x[2]))  # cheaper per-lane, then more lanes, then larger length_limit
            _, chosen, Llim, lanes = candidates[0]
            # Remove chosen from unused
            unused.remove(chosen)
            # Place this vehicle consuming one lane
            open_bins.append((chosen, Llim, lanes - 1))

        # Extract used listings in order of opening; this is already minimal by lanes strategy
        used_listings = [lst for (lst, _, _) in open_bins]
        return used_listings

    @staticmethod
    def calculate_total_price(listings: List[Listing]) -> int:
        return sum(listing.price_in_cents for listing in listings)