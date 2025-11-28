# Calcagnini Trails - Offline PWA Trail Map

A **100% offline** trail map for the Calcagnini Contemplative Center in Bluemont, VA. 
No internet required after initial install.

## Features

- **Truly Offline**: Map tiles are bundled with the app - works without any internet
- **GPS Tracking**: Real-time "you are here" positioning
- **Installable**: Can be added to phone home screen like a native app
- **Contemplative Design**: Muted, nature-focused color palette

---

## Setup Instructions

### Step 1: Download the Map Tiles

The tiles are NOT included in this repository because they're ~10-15MB of image files.
You need to download them once using the provided script.

**Requirements:** Python 3 with `requests` library

```bash
# Install requests if you don't have it
pip install requests

# Run the tile downloader
python download_tiles.py
```

This will create a `tiles/` folder with ~579 PNG files organized by zoom level.
Takes about 2-3 minutes depending on your connection.

**Tile Coverage:**
- Zoom levels: 14-18
- Area: ~1.9km × 1.9km around the retreat center
- Total size: ~10-15 MB

### Step 2: Verify Your File Structure

After downloading tiles, your folder should look like this:

```
calcagnini-trails/
├── index.html
├── manifest.json
├── service-worker.js
├── download_tiles.py
├── README.md
├── icons/
│   ├── icon-192.png
│   └── icon-512.png
└── tiles/
    ├── 14/
    │   └── 4648/
    │       └── 6254.png (etc.)
    ├── 15/
    ├── 16/
    ├── 17/
    └── 18/
```

### Step 3: Deploy to GitHub Pages

1. Create a new repository on GitHub (e.g., `calcagnini-trails`)
2. Upload ALL files including the `tiles/` folder
3. Go to Settings → Pages
4. Set Source to `main` branch, `/ (root)` folder
5. Save and wait 1-2 minutes

Your map will be live at: `https://[your-username].github.io/calcagnini-trails/`

---

## For Retreat Guests

### Installing the App

**iPhone/iPad (Safari only):**
1. Open Safari and go to the map URL
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Tap "Add"

**Android (Chrome):**
1. Open Chrome and go to the map URL
2. Tap the menu (three dots)
3. Tap "Add to Home Screen" or "Install App"
4. Tap "Add"

**Important:** The map works offline immediately - no need to pre-cache anything.
Just install and go!

### Using the Map

- **Find Me**: Tap to show your GPS location (red pulsing dot)
- **Trail**: Tap to re-center on the Magis Loop trail
- **?**: Tap for help and installation instructions

If you feel lost, the red dot always shows your real position. 
Follow the trail line back toward the Contemplative Center.

---

## Customization

### Adding More Trails

1. Walk the trail with a GPS app (like Organic Maps) recording
2. Export as GPX file
3. Convert coordinates to the JavaScript array format in `index.html`
4. Add a new `L.polyline()` with a different color

Example:
```javascript
const newTrailCoords = [
    [39.1055, -77.8600],
    [39.1060, -77.8605],
    // ... more coordinates
];

const newTrail = L.polyline(newTrailCoords, {
    color: '#4a7c6f',  // Different color
    weight: 5,
    opacity: 0.9
}).addTo(map);
```

### Adding Points of Interest

Add markers for meditation spots, story locations, etc:

```javascript
const poiIcon = L.divIcon({
    className: 'poi-marker',
    html: '🧘',
    iconSize: [24, 24]
});

L.marker([39.1065, -77.8610], { icon: poiIcon })
    .addTo(map)
    .bindPopup('<h4>Meditation Rock</h4><p>A quiet spot for reflection.</p>');
```

### Changing the Map Style

The current tiles use standard OpenStreetMap style. For a different look:

1. Use a different tile server in `download_tiles.py`:
   - OpenTopoMap: `https://tile.opentopomap.org/{z}/{x}/{y}.png`
   - Stamen Terrain: `https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png`
   
2. Re-run the download script
3. Replace the tiles folder

---

## Technical Details

### Bounding Box

Based on your FULL_MAP.kmz:
- North: 39.119012
- South: 39.097729  
- East: -77.841725
- West: -77.868256

### Tile Math

| Zoom | Tiles | Purpose |
|------|-------|---------|
| 14 | 4 | Regional overview |
| 15 | 9 | Area context |
| 16 | 36 | Trail visible |
| 17 | 110 | Good detail |
| 18 | 420 | Full navigation detail |
| **Total** | **579** | **~10-15 MB** |

### Property Boundary (from RETREAT.kmz)

The retreat property is marked in the code but not visually displayed.
Coordinates available if you want to add a boundary overlay.

---

## Version 2 Ideas

- **iNaturalist Integration**: Camera button to identify plants/animals
- **Story Points**: POIs with reflections, poems, or guided meditations  
- **Seasonal Content**: Different POI content for different times of year
- **Second Trail**: Add when GPX is recorded

---

## Troubleshooting

**Map tiles not loading:**
- Verify `tiles/` folder is in the same directory as `index.html`
- Check browser console for 404 errors
- Ensure all zoom level folders (14-18) are present

**GPS not working:**
- Ensure location permissions are granted
- Try outdoors with clear sky view
- Some browsers restrict GPS on non-HTTPS sites

**Can't install to home screen:**
- iPhone: Must use Safari (not Chrome)
- Ensure site is served over HTTPS (GitHub Pages does this automatically)

---

## License

- Code: MIT License
- Map tiles: © OpenStreetMap contributors (ODbL)
- Trail data: Property of Georgetown University

---

## Credits

Built for the Calcagnini Contemplative Center at Georgetown University.
