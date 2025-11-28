# Calcagnini Trails PWA - Project Requirements Document

## Project Overview

**Project Name:** Calcagnini Trails  
**Type:** Progressive Web App (PWA)  
**Purpose:** 100% offline trail map with GPS tracking for retreat center guests  
**Location:** Calcagnini Contemplative Center, 400 Loyola Ln, Bluemont, VA 20135  
**Property Owner:** Georgetown University

---

## Current Project Status

### ✅ COMPLETED

| Item | Status | Notes |
|------|--------|-------|
| Core PWA structure | Done | index.html, manifest.json, service-worker.js |
| Leaflet.js map integration | Done | Using local tile paths |
| GPS "you are here" tracking | Done | Pulsing red dot with accuracy display |
| Magis Loop trail overlay | Done | 79 GPS points from GPX file |
| Contemplative UI design | Done | Muted forest/earth color palette |
| Help modal with install instructions | Done | iOS and Android instructions |
| Offline detection banner | Done | Shows when offline |
| App icons | Done | 192px and 512px PNG |
| Tile download script | Done | Python script ready to run |
| Bounding box calculated | Done | From KMZ files |

### 🔄 IN PROGRESS - NEEDS COMPLETION

| Item | Status | What's Needed |
|------|--------|---------------|
| Map tiles | **NOT DOWNLOADED** | Run `download_tiles.py` to download 579 tiles (~10-15MB) |
| GitHub deployment | Partial | Files uploaded, but tiles folder is empty |
| GitHub Pages | Not enabled | Enable in repo Settings → Pages |

### 📋 FUTURE (Version 2)

| Item | Priority | Notes |
|------|----------|-------|
| Points of Interest (POIs) | High | Meditation spots, story locations |
| Second trail | High | Need to walk and record GPX |
| iNaturalist integration | Medium | Camera for plant/animal ID |
| Custom building overlay | Low | Illustrated map of center |

---

## Technical Architecture

### File Structure (Target State)

```
calcagnini-trails/
├── index.html              ✅ Complete
├── manifest.json           ✅ Complete
├── service-worker.js       ✅ Complete
├── download_tiles.py       ✅ Complete (needs to be RUN)
├── README.md               ✅ Complete
├── icons/
│   ├── icon-192.png        ✅ Complete
│   └── icon-512.png        ✅ Complete
└── tiles/                  ⚠️  EMPTY - NEEDS TILES DOWNLOADED
    ├── 14/                 
    │   ├── 4648/
    │   │   ├── 6254.png
    │   │   └── 6255.png
    │   └── 4649/
    │       ├── 6254.png
    │       └── 6255.png
    ├── 15/                 (9 tiles)
    ├── 16/                 (36 tiles)
    ├── 17/                 (110 tiles)
    └── 18/                 (420 tiles)
```

### Technology Stack

| Component | Technology | Version/CDN |
|-----------|------------|-------------|
| Mapping Library | Leaflet.js | 1.9.4 via unpkg CDN |
| Tile Format | PNG raster tiles | OSM standard z/x/y format |
| Offline | Service Worker | Cache-first strategy |
| Install | PWA Manifest | Standalone display mode |
| Styling | Vanilla CSS | Custom properties for theming |

---

## Geographic Data

### Bounding Box (Full Map Coverage)

Extracted from `FULL_MAP.kmz`:

```
North: 39.119012
South: 39.097729
East:  -77.841725
West:  -77.868256
```

**Coverage Area:** ~1.9km × 1.9km (~908 acres)

### Retreat Property Boundary

Extracted from `RETREAT.kmz`:

```
North: 39.108980
South: 39.100014
East:  -77.853710
West:  -77.863937
```

**Property Size:** 55 acres

### Tile Requirements

| Zoom | X Range | Y Range | Count | Purpose |
|------|---------|---------|-------|---------|
| 14 | 4648-4649 | 6254-6255 | 4 | Regional context |
| 15 | 9296-9298 | 12509-12511 | 9 | Area overview |
| 16 | 18592-18597 | 25018-25023 | 36 | Trail visible |
| 17 | 37185-37194 | 50037-50047 | 110 | Good detail |
| 18 | 74370-74389 | 100074-100094 | 420 | Navigation detail |
| **TOTAL** | | | **579** | **~10-15 MB** |

### Trail Data: Magis Loop

**Source:** `First_round_walk.gpx` recorded with Organic Maps  
**Points:** 79 GPS coordinates with elevation  
**Elevation Range:** 364m - 439m (75m gain/loss)  
**Estimated Time:** 30-45 minutes at contemplative pace

**Coordinates (already embedded in index.html):**
```javascript
const magisLoopCoords = [
    [39.105523, -77.85928],   // Start point
    [39.105592, -77.859392],
    // ... 77 more points ...
    [39.104885, -77.860774]   // End point
];
```

### Center Location (Contemplative Center Building)

```javascript
const centerLocation = [39.1052, -77.8595];
```

---

## Immediate Next Steps

### Step 1: Download Map Tiles

The tiles are the critical missing piece. Run this on a computer with Python:

```bash
# Navigate to project folder
cd calcagnini-trails

# Install dependency
pip install requests

# Run downloader (takes 2-3 minutes)
python download_tiles.py
```

**What this does:**
- Connects to OpenStreetMap tile servers
- Downloads 579 PNG tiles for your bounding box
- Organizes them into `tiles/{z}/{x}/{y}.png` structure
- Shows progress and final size

### Step 2: Verify Tiles Downloaded

After running, check:
```bash
# Should show ~579 files
find tiles -name "*.png" | wc -l

# Should be 10-15 MB
du -sh tiles/
```

### Step 3: Push Tiles to GitHub

```bash
git add tiles/
git commit -m "Add offline map tiles"
git push
```

### Step 4: Enable GitHub Pages

1. Go to repository Settings
2. Click "Pages" in sidebar
3. Source: `main` branch, `/ (root)` folder
4. Save
5. Wait 1-2 minutes for deployment

### Step 5: Test

1. Open `https://YOUR_USERNAME.github.io/calcagnini-trails/` on phone
2. Tap "Find Me" to test GPS
3. Add to home screen
4. Turn on airplane mode
5. Verify map still works

---

## Design Specifications

### Color Palette

```css
/* Nature-focused muted palette */
--forest-deep: #2d4a3e;     /* Primary brand, headers */
--forest-mid: #4a7c6f;      /* Accent, buttons */
--forest-light: #7da99a;    /* Hover states */
--forest-pale: #c8ddd5;     /* Backgrounds */
--earth-warm: #8b7355;      /* Secondary accent */
--earth-light: #d4c4b0;     /* Subtle backgrounds */
--stone: #9a9a8e;           /* Neutral */

/* Trail colors */
--trail-magis: #c97b4a;     /* Orange-brown for Magis Loop */
--trail-secondary: #4a7c6f; /* Green for future trails */
--you-are-here: #d94f4f;    /* Red for GPS marker */
```

### Typography

- Font: System fonts (-apple-system, BlinkMacSystemFont, etc.)
- Header: 18px, weight 600
- Body: 14px, weight 400
- Small: 12-13px

### Spacing

- 8px base unit
- Padding: 12-24px
- Border radius: 8-24px (rounded, friendly)

### UI Components

| Component | Style |
|-----------|-------|
| Header | Fixed, white with blur, subtle border |
| Buttons | Rounded pills, subtle shadows |
| GPS Status | Pill badge, top-right |
| Legend | Rounded card, bottom-left |
| Controls | Centered bottom, floating buttons |
| Modal | Centered overlay, rounded card |

---

## Code Reference

### Key JavaScript Functions

```javascript
// Initialize map (called after Leaflet loads)
function initMap() { ... }

// Toggle GPS tracking on/off
function toggleTracking() { ... }

// Update GPS status display
function updateGPSStatus(status, isActive, isError) { ... }

// Create pulsing user location marker
function createUserMarker(latlng) { ... }

// Center map on trail bounds
function centerOnTrail() { ... }

// Show/close help modal
function showHelp() { ... }
function closeHelp() { ... }
```

### Service Worker Strategy

- **Install:** Cache core files (HTML, CSS, JS libraries)
- **Fetch:** Cache-first for all requests
- **Tiles:** Served from local `/tiles/` folder, cached on first load
- **Offline:** Return cached index.html for navigation requests

---

## Future Features (Version 2 Scope)

### Points of Interest System

```javascript
// POI data structure
const pois = [
    {
        id: 'meditation-rock',
        name: 'Meditation Rock',
        coords: [39.1065, -77.8610],
        icon: '🧘',
        type: 'meditation',
        content: {
            title: 'Meditation Rock',
            description: 'A quiet spot for reflection...',
            reflection: 'Take three deep breaths...'
        }
    },
    // ... more POIs
];
```

### Second Trail

Need to:
1. Walk trail with Organic Maps recording
2. Export GPX
3. Convert to coordinate array
4. Add to index.html with different color

### iNaturalist Integration

Button that opens iNaturalist app with pre-filled location:
```javascript
function openINaturalist() {
    const url = `https://www.inaturalist.org/observations/new?lat=${userLat}&lng=${userLng}`;
    window.open(url, '_blank');
}
```

---

## Testing Checklist

### Functionality
- [ ] Map loads with tiles visible
- [ ] Trail line displays correctly
- [ ] GPS "Find Me" works and shows location
- [ ] GPS accuracy displays
- [ ] "Trail" button recenters on trail
- [ ] Help modal opens and closes
- [ ] Map bounds prevent scrolling too far

### Offline
- [ ] App works in airplane mode after initial load
- [ ] "You're offline" banner appears
- [ ] GPS still works offline
- [ ] All tiles load offline

### PWA
- [ ] "Add to Home Screen" works on iOS Safari
- [ ] "Install App" works on Android Chrome
- [ ] App icon appears correctly
- [ ] Opens in standalone mode (no browser chrome)
- [ ] Theme color applies to status bar

### Cross-Device
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] iPad
- [ ] Android tablet

---

## Repository Information

**GitHub URL:** (your repo URL here)  
**GitHub Pages URL:** `https://YOUR_USERNAME.github.io/calcagnini-trails/`

---

## Contact / Context

**Property Manager:** g (current user)  
**Location:** Calcagnini Contemplative Center, Bluemont, VA  
**Supervisor:** Donna Poillucci  
**Owner:** Georgetown University

---

## Summary for AI Coding Tools

**What this project is:** A Progressive Web App that displays an offline trail map with GPS tracking for a retreat center.

**What's done:** All code is complete. The app structure, UI, GPS tracking, trail overlay, and tile download script are finished.

**What's needed to make it work:** 
1. Run `python download_tiles.py` to download 579 map tiles from OpenStreetMap
2. Commit and push the tiles folder to GitHub
3. Enable GitHub Pages

**The single blocker:** The `tiles/` folder is empty. The download script exists but hasn't been executed yet.

After tiles are downloaded and deployed, the app will be 100% functional offline.
