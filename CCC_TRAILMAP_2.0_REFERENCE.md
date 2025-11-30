# CCC.TRAILMAP 2.0 - Working Reference Copy

**Version:** 2.0  
**Date:** November 30, 2025  
**Status:** ✅ FULLY FUNCTIONAL OFFLINE PWA  
**Repository:** BraveNewEarth/CCC.TRAILMAP

---

## 🎯 Project Summary

CCC.TRAILMAP is a **100% offline-capable Progressive Web App** for the Calcagnini Contemplative Center in Bluemont, VA. It provides GPS-enabled trail navigation that works completely without internet connectivity after initial installation.

### Key Achievements (Version 2.0)

- ✅ **Fully Offline**: 767 map tiles cached locally via service worker
- ✅ **GPS Tracking**: Real-time "you are here" positioning with accuracy display
- ✅ **Auto-Start GPS**: Automatically begins tracking on page load
- ✅ **Trail Overlay**: Magis Loop trail with 79 GPS waypoints
- ✅ **PWA Installable**: Add to home screen on iOS and Android
- ✅ **Contemplative Design**: Nature-focused muted color palette
- ✅ **Offline Detection**: Banner alerts when offline (map still works)
- ✅ **Bounds Protection**: Prevents users from scrolling too far from trail area

---

## 📁 Project Structure

```
CCC.TRAILMAP/
├── index.html                  # Main PWA application (883 lines)
├── manifest.json               # PWA manifest for installation
├── service-worker.js           # Aggressive tile caching for offline use
├── download_tiles.py           # Python script to download map tiles
├── README.md                   # User-facing documentation
├── CALCAGNINI_TRAILS_PRD.md    # Product Requirements Document
├── CCC_TRAILMAP_2.0_REFERENCE.md  # This file
├── .gitignore                  # Git ignore rules
├── .gitattributes              # Git attributes
├── icons/
│   ├── icon-192.png            # PWA icon (192x192)
│   └── icon-512.png            # PWA icon (512x512)
├── tiles/                      # 767 offline map tiles (cached via SW)
│   ├── 14/                     # Zoom level 14 (regional)
│   ├── 15/                     # Zoom level 15 (area)
│   ├── 16/                     # Zoom level 16 (trail visible)
│   ├── 17/                     # Zoom level 17 (good detail)
│   └── 18/                     # Zoom level 18 (navigation detail)
├── archiveFolder/              # Archive of previous versions
└── Prototypeexample.png        # Design prototype reference
```

---

## 🚀 Technical Architecture

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Mapping Library | Leaflet.js | 1.9.4 (CDN) |
| Tile Source | OpenStreetMap | Standard tiles |
| Offline Strategy | Service Worker | Cache-first with aggressive caching |
| PWA Manifest | manifest.json | Standalone display mode |
| Styling | Vanilla CSS | CSS custom properties |
| GPS API | Geolocation API | watchPosition with high accuracy |

### Offline Architecture

**Service Worker Strategy:**
1. **Install Phase**: Cache core files (HTML, manifest, icons)
2. **Fetch Phase**: Cache-first for all requests
3. **Tile Caching**: Aggressive caching of OSM tiles on first load
4. **Fallback**: Return cached index.html for navigation requests

**Tile Coverage:**
- **Total Tiles**: 767 PNG files
- **Zoom Levels**: 14-18
- **Bounding Box**: 
  - North: 39.119012
  - South: 39.097729
  - East: -77.841725
  - West: -77.868256
- **Coverage Area**: ~1.9km × 1.9km (~908 acres)

---

## 🗺️ Geographic Data

### Retreat Center Location
```javascript
const centerLocation = [39.1052, -77.8595];
// Address: 400 Loyola Ln, Bluemont, VA 20135
```

### Magis Loop Trail
- **Total Points**: 79 GPS coordinates
- **Elevation Range**: 364m - 439m (75m gain/loss)
- **Estimated Time**: 30-45 minutes at contemplative pace
- **Trail Color**: `#c97b4a` (orange-brown)
- **Trail Weight**: 5px line width

### Property Boundaries

**Full Map Coverage (FULL_MAP.kmz):**
```
North: 39.119012
South: 39.097729
East:  -77.841725
West:  -77.868256
```

**Retreat Property (RETREAT.kmz):**
```
North: 39.108980
South: 39.100014
East:  -77.853710
West:  -77.863937
Property Size: 55 acres
```

---

## 🎨 Design System

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
- **Font Stack**: System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto)
- **Header**: 18px, weight 600
- **Body**: 14px, weight 400
- **Small**: 12-13px

### UI Components
- **Header**: Fixed, white with blur backdrop, subtle border
- **Buttons**: Rounded pills (24px radius), subtle shadows
- **GPS Status**: Pill badge, top-right, pulsing green dot when active
- **Legend**: Rounded card (12px radius), bottom-left
- **Controls**: Centered bottom, floating buttons
- **Modal**: Centered overlay, rounded card (16px radius)

---

## 💻 Key Code Components

### Core JavaScript Functions

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

// Check if user is within map bounds
function isWithinBounds(lat, lng) { ... }
```

### GPS Tracking Features

1. **Auto-Start**: GPS begins tracking automatically on page load
2. **High Accuracy**: Enabled for better positioning
3. **Continuous Tracking**: Uses `watchPosition` for real-time updates
4. **Accuracy Display**: Shows GPS accuracy in meters
5. **Bounds Checking**: Alerts if user is outside mapped area
6. **Pulsing Marker**: Red dot with animated pulse ring

### Service Worker Caching

```javascript
// Cache-first strategy with aggressive tile caching
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            if (response) {
                return response; // Return cached version
            }
            return fetch(event.request).then((response) => {
                // Cache OSM tiles aggressively
                if (event.request.url.includes('tile.openstreetmap.org')) {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return response;
            });
        })
    );
});
```

---

## 📝 Git History (Recent Commits)

```
4c325bc (HEAD -> main) Add attributionControl: false and debug logging
e19c5de Implement hybrid offline tiles with aggressive service worker caching
11a5225 Add edge tiles with 1-tile buffer for complete offline coverage
8fa0b03 Switch to local offline tiles with strict bounds for safety
3a3d409 Use online tiles (local tiles don't work on GitHub Pages)
92f99a0 Restore working map with local tiles + add auto-start GPS
c024132 Switch to online OSM tiles to fix grey map
b69ef78 Fix watchPosition syntax error causing blank screen
332770d Fix GPS: auto-start, high accuracy, and off-map alerts
```

### Key Evolution Points

1. **Initial Build**: Basic PWA structure with local tiles
2. **GPS Issues**: Fixed blank screen and GPS tracking bugs
3. **Offline Strategy**: Switched from local tiles to service worker caching
4. **Auto-Start GPS**: Added automatic GPS tracking on load
5. **Bounds Protection**: Added alerts for users outside mapped area
6. **Aggressive Caching**: Implemented cache-first strategy for true offline use

---

## ✅ Testing Checklist

### Functionality
- [x] Map loads with tiles visible
- [x] Trail line displays correctly
- [x] GPS "Find Me" works and shows location
- [x] GPS auto-starts on page load
- [x] GPS accuracy displays in real-time
- [x] "Trail" button recenters on trail
- [x] Help modal opens and closes
- [x] Map bounds prevent scrolling too far
- [x] Out-of-bounds alerts work

### Offline
- [x] App works in airplane mode after initial load
- [x] "You're offline" banner appears when offline
- [x] GPS still works offline
- [x] All tiles load offline from cache
- [x] Service worker caches tiles aggressively

### PWA
- [x] "Add to Home Screen" works on iOS Safari
- [x] "Install App" works on Android Chrome
- [x] App icon appears correctly
- [x] Opens in standalone mode (no browser chrome)
- [x] Theme color applies to status bar

---

## 🔮 Future Enhancements (Version 3.0)

### High Priority
- [ ] **Points of Interest (POIs)**: Meditation spots, story locations
- [ ] **Second Trail**: Walk and record GPX for additional trail
- [ ] **Trail Statistics**: Distance, elevation gain, estimated time

### Medium Priority
- [ ] **iNaturalist Integration**: Camera button for plant/animal ID
- [ ] **Seasonal Content**: Different POI content for different seasons
- [ ] **Offline Audio**: Guided meditations at specific locations
- [ ] **Trail Conditions**: User-submitted trail condition reports

### Low Priority
- [ ] **Custom Building Overlay**: Illustrated map of center buildings
- [ ] **Multi-language Support**: Spanish, French translations
- [ ] **Dark Mode**: Night-friendly color scheme
- [ ] **Trail Sharing**: Share trail progress with friends

---

## 🛠️ Deployment Information

### GitHub Pages
- **Repository**: BraveNewEarth/CCC.TRAILMAP
- **Branch**: main
- **Source**: / (root)
- **URL**: `https://[username].github.io/CCC.TRAILMAP/`

### Installation Instructions

**For Developers:**
1. Clone repository
2. Run `python download_tiles.py` (if tiles not present)
3. Serve locally or deploy to GitHub Pages

**For Users:**
1. Visit the GitHub Pages URL
2. Tap "Find Me" to enable GPS
3. Add to home screen (iOS: Share → Add to Home Screen)
4. Use offline anytime

---

## 📊 Project Metrics

| Metric | Value |
|--------|-------|
| Total Lines of Code | ~1,200 |
| Map Tiles | 767 PNG files |
| Tile Storage | ~10-15 MB |
| GPS Waypoints | 79 coordinates |
| Zoom Levels | 5 (14-18) |
| Coverage Area | ~908 acres |
| Trail Length | ~1.5 km |
| Development Time | ~3 weeks |

---

## 🤝 Credits & License

**Built For**: Calcagnini Contemplative Center, Georgetown University  
**Location**: 400 Loyola Ln, Bluemont, VA 20135  
**Property Manager**: Bruce Weaver  
**Supervisor**: Donna Poillucci  
**Owner**: Georgetown University

**License:**
- Code: MIT License
- Map Tiles: © OpenStreetMap contributors (ODbL)
- Trail Data: Property of Georgetown University

---

## 📞 Support & Contact

For issues, questions, or feature requests:
1. Check the [README.md](README.md) for troubleshooting
2. Review the [PRD](CALCAGNINI_TRAILS_PRD.md) for technical details
3. Contact property manager for access or permissions

---

## 🔒 Version Lock

This document represents the **working reference copy** of CCC.TRAILMAP 2.0 as of **November 30, 2025**.

**Key Features Locked:**
- ✅ Fully offline PWA with service worker caching
- ✅ Auto-start GPS tracking
- ✅ 767 cached map tiles
- ✅ Magis Loop trail overlay
- ✅ Contemplative design system
- ✅ Installable on iOS and Android

**Known Working State:**
- Commit: `4c325bc`
- Branch: `main`
- Status: Production-ready
- Tested: iOS Safari, Android Chrome

---

*This reference document serves as the definitive snapshot of CCC.TRAILMAP 2.0 functionality and architecture.*
