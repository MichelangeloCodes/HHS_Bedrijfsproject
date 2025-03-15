import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar
import time

# Constanten
PORT_NAME = 'COM9'  # Vervang dit door de juiste poort van je RPLidar
MAX_DISTANCE_CM = 400 # De max afstand die de lidar kan meten in cm
WALL_DISTANCE_THRESHOLD_CM = 30  # De minimale afstand om als muur te beschouwen
POINT_DENSITY_THRESHOLD = 30  # De hoeveelheid punten per vierkante cm om iets als muur te beschouwen
WALL_MINIMUM_POINTS = 3  # Minimum aantal punten per wall segment om mee te tellen als een muur segment

def filter_walls(scan):
    """Filtert de punten uit een RPLidar scan en geeft de muren terug."""
    wall_points = []

    for _, angle, distance in scan:
        if distance > 0 and distance <= MAX_DISTANCE_CM:
            # Zet de polar coordinaten om naar cartesian
            x = distance * np.cos(np.radians(angle))
            y = distance * np.sin(np.radians(angle))
            
            wall_points.append([x/100,y/100]) # We veranderen naar meter

    # Converteer naar numpy array
    wall_points = np.array(wall_points)
    if len(wall_points) == 0:
        return np.array([])
    
    # We groeperen de points
    grouped_points = group_points(wall_points, WALL_DISTANCE_THRESHOLD_CM/100)

    # Filteren op wall dichtheid
    filtered_wall_points = []
    for group in grouped_points:
       
       if len(group) > WALL_MINIMUM_POINTS: # Kijken of er genoeg punten zijn
            # Bereken de afstand tussen de punten.
            x_min = np.min(group[:, 0])
            x_max = np.max(group[:, 0])
            y_min = np.min(group[:, 1])
            y_max = np.max(group[:, 1])
            
            area = (x_max-x_min) * (y_max-y_min)
            
            points_per_cm = len(group)/area if area > 0 else 0
            
            if points_per_cm > POINT_DENSITY_THRESHOLD: # Kijken of de dichtheid groot genoeg is.
                 filtered_wall_points += group.tolist()

    
    return np.array(filtered_wall_points) if len(filtered_wall_points) > 0 else np.array([])

def group_points(points, threshold):
    """Groupt de dicht bij elkaar liggende punten."""
    if len(points) == 0:
         return []
    
    groups = []
    used = [False] * len(points)

    for i, point in enumerate(points):
        if not used[i]:
            group = [point]
            used[i] = True
            
            queue = [i]
            while queue:
                current_index = queue.pop(0)
                for j, other_point in enumerate(points):
                    if not used[j]:
                        distance = np.linalg.norm(points[current_index] - other_point)
                        if distance < threshold:
                            group.append(other_point)
                            used[j] = True
                            queue.append(j)
            groups.append(np.array(group))

    return groups

def main():
    """Main functie"""
    lidar = None
    try:
        # Maak verbinding met de Lidar
        lidar = RPLidar(PORT_NAME)

        # Start de scan
        lidar.start_motor()
        time.sleep(1) # Wacht tot de lidar up is

        # Scan en toon data
        for _ in range(50): # Scan 50 keer en dan stopt het. Dit kan veranderd worden.
            scan = lidar.iter_scans()
            
            all_wall_points = np.array([])
            
            for _, one_scan in enumerate(scan):
                 wall_points = filter_walls(one_scan)
                 if len(wall_points) > 0:
                     if len(all_wall_points) == 0:
                        all_wall_points = wall_points
                     else:
                        all_wall_points = np.concatenate((all_wall_points, wall_points))
            
            if len(all_wall_points) > 0:
                # Plot de gefilterde punten
                plt.figure(figsize=(8, 8))
                plt.scatter(all_wall_points[:, 0], all_wall_points[:, 1], s=5, label='Muren', color = 'black')
                plt.xlabel("X (m)")
                plt.ylabel("Y (m)")
                plt.title("Muren kaart met RPLidar A1")
                plt.grid(True)
                plt.axis('equal') # De x en y schalen gelijk maken
                plt.legend()
                plt.show(block = False)
                plt.pause(0.1)
                plt.clf()
            else:
                print("Geen muren gevonden.")

        print("Scan is gestopt")

    except Exception as e:
        print(f"Fout: {e}")
    finally:
        if lidar:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            print("Lidar is disconnected")

if __name__ == '__main__':
    main()