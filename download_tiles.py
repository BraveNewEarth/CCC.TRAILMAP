#!/usr/bin/env python3
"""
Tile Downloader for Calcagnini Trails PWA
==========================================

This script downloads OpenStreetMap tiles for offline use in the trail map app.
Run this on your own computer with internet access.

Requirements:
    pip install requests

Usage:
    python download_tiles.py

The script will create a 'tiles' folder with all necessary map tiles.
"""

import os
import math
import requests
import time
import sys

# =============================================================================
# CONFIGURATION - Based on your FULL_MAP.kmz boundaries
# =============================================================================

BOUNDS = {
    'north': 39.119012,
    'south': 39.097729,
    'east': -77.841725,
    'west': -77.868256
}

ZOOM_LEVELS = [14, 15, 16, 17, 18]

OUTPUT_DIR = 'tiles'

# Tile server - using OSM standard tiles
# You can also use other tile servers that permit downloading
TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

# Be respectful to OSM servers
DELAY_BETWEEN_REQUESTS = 0.15  # seconds
USER_AGENT = 'CalcagniniTrailsPWA/1.0 (offline trail map for retreat center)'

# =============================================================================
# TILE MATH FUNCTIONS
# =============================================================================

def deg2num(lat_deg, lon_deg, zoom):
    """Convert lat/lon to tile numbers"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def get_tile_bounds(zoom, bounds):
    """Get tile coordinate ranges for a bounding box at a zoom level"""
    nw = deg2num(bounds['north'], bounds['west'], zoom)
    se = deg2num(bounds['south'], bounds['east'], zoom)
    
    x_min = min(nw[0], se[0])
    x_max = max(nw[0], se[0])
    y_min = min(nw[1], se[1])
    y_max = max(nw[1], se[1])
    
    # Add 1-tile buffer on each side to ensure Leaflet has all tiles it needs
    x_min -= 1
    x_max += 1
    y_min -= 1
    y_max += 1
    
    return x_min, x_max, y_min, y_max

# =============================================================================
# DOWNLOAD FUNCTIONS
# =============================================================================

def download_tile(z, x, y, output_dir):
    """Download a single tile"""
    tile_dir = os.path.join(output_dir, str(z), str(x))
    os.makedirs(tile_dir, exist_ok=True)
    
    tile_path = os.path.join(tile_dir, f"{y}.png")
    
    # Skip if already downloaded
    if os.path.exists(tile_path):
        return True, "exists"
    
    url = TILE_URL.format(z=z, x=x, y=y)
    headers = {'User-Agent': USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(tile_path, 'wb') as f:
                f.write(response.content)
            return True, "downloaded"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def calculate_totals():
    """Calculate total tiles needed"""
    total = 0
    details = []
    for zoom in ZOOM_LEVELS:
        x_min, x_max, y_min, y_max = get_tile_bounds(zoom, BOUNDS)
        count = (x_max - x_min + 1) * (y_max - y_min + 1)
        total += count
        details.append((zoom, count))
    return total, details

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("Calcagnini Trails - Tile Downloader")
    print("=" * 60)
    print()
    print(f"Bounding Box:")
    print(f"  North: {BOUNDS['north']}")
    print(f"  South: {BOUNDS['south']}")
    print(f"  East:  {BOUNDS['east']}")
    print(f"  West:  {BOUNDS['west']}")
    print()
    
    total_tiles, details = calculate_totals()
    
    print("Tiles to download:")
    for zoom, count in details:
        print(f"  Zoom {zoom}: {count} tiles")
    print(f"  TOTAL: {total_tiles} tiles")
    print(f"  Estimated size: {total_tiles * 15 // 1024} - {total_tiles * 25 // 1024} MB")
    print()
    
    # Confirm before downloading
    response = input("Proceed with download? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    print()
    print("Downloading tiles...")
    print()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    downloaded = 0
    skipped = 0
    failed = 0
    
    for zoom in ZOOM_LEVELS:
        x_min, x_max, y_min, y_max = get_tile_bounds(zoom, BOUNDS)
        zoom_total = (x_max - x_min + 1) * (y_max - y_min + 1)
        zoom_done = 0
        
        print(f"Zoom {zoom} ({zoom_total} tiles)...")
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                success, msg = download_tile(zoom, x, y, OUTPUT_DIR)
                
                if success:
                    if msg == "exists":
                        skipped += 1
                    else:
                        downloaded += 1
                else:
                    failed += 1
                    print(f"  FAILED: {zoom}/{x}/{y} - {msg}")
                
                zoom_done += 1
                
                # Progress indicator
                if zoom_done % 50 == 0:
                    pct = zoom_done / zoom_total * 100
                    print(f"  Progress: {zoom_done}/{zoom_total} ({pct:.0f}%)")
                
                # Rate limiting
                if msg == "downloaded":
                    time.sleep(DELAY_BETWEEN_REQUESTS)
        
        print(f"  Done.")
    
    # Calculate total size
    total_size = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))
    
    print()
    print("=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"Downloaded: {downloaded}")
    print(f"Already existed: {skipped}")
    print(f"Failed: {failed}")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    print()
    print(f"Tiles saved to: {os.path.abspath(OUTPUT_DIR)}/")
    print()
    print("Next step: Copy the 'tiles' folder into your PWA directory")
    print("alongside index.html, then deploy to GitHub Pages.")

if __name__ == '__main__':
    main()
