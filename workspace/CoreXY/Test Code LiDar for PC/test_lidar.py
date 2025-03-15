from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import time

# Poort waarop de Lidar is aangesloten
PORT_NAME = 'COM9'

# Verwachte afstand en marge voor metingen
EXPECTED_DISTANCE = 6000
TOLERANCE = 2000
TARGET_ANGLE = 0  # Hoek in graden
ANGLE_TOLERANCE = 2
NUM_MEASUREMENTS = 100

# Posities rondom de x-as voor muurhoekberekening
X_POSITIONS = [-200, 200]

# Functies voor conversies en berekeningen
def polar_to_cartesian(angle, distance):
    """Converteert polaire coördinaten naar cartesische coördinaten."""
    angle_rad = np.radians(angle)
    x = distance * np.cos(angle_rad)
    y = distance * np.sin(angle_rad)
    return x, y

def find_closest_points(points, x_target, num_points=5):
    """Zoekt de `num_points` dichtstbijzijnde punten bij x_target."""
    sorted_points = sorted(points, key=lambda p: abs(p[0] - x_target))
    return sorted_points[:num_points]

def calculate_average_point(points):
    """Bereken het gemiddelde van een lijst punten."""
    if not points:
        return None
    x_avg = np.mean([p[0] for p in points])
    y_avg = np.mean([p[1] for p in points])
    return (x_avg, y_avg)

def calculate_angle_between_points(point1, point2):
    """Bereken de hoek tussen de lijn door twee punten en de x-as."""
    if point1 is None or point2 is None:
        return None
    x1, y1 = point1
    x2, y2 = point2
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle = np.degrees(np.arctan2(delta_y, delta_x))
    return angle

MAX_ANGLE_THRESHOLD = 10  # Maximale toegestane hoek (graden)

def main():
    lidar = RPLidar(PORT_NAME)
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-5000, 5000)
    ax.set_ylim(-5000, 5000)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    scatter = ax.scatter([], [])
    recent_distances = []
    recent_angles = []

    try:
        print("Starting measurements. Press Ctrl+C to stop.")
        for scan in lidar.iter_scans():
            points = []
            valid_distances = []

            for (_, angle, distance) in scan:
                if distance > 0:
                    y, x = polar_to_cartesian(angle, distance)
                    points.append((x, y))

                # Filter op 0 graden voor afstandsmeting
                if abs(angle - TARGET_ANGLE) <= ANGLE_TOLERANCE:
                    if EXPECTED_DISTANCE - TOLERANCE <= distance <= EXPECTED_DISTANCE + TOLERANCE:
                        valid_distances.append(distance)

            # Update scatter plot
            if points:
                scatter.set_offsets(points)
                plt.draw()
                plt.pause(0.01)

            # Bereken afstand op 0 graden
            if valid_distances:
                closest_distance = min(valid_distances, key=lambda d: abs(d - EXPECTED_DISTANCE))
                recent_distances.append(closest_distance)
                if len(recent_distances) > NUM_MEASUREMENTS:
                    recent_distances.pop(0)
                average_distance = sum(recent_distances) / len(recent_distances)
                print(f"Gemiddelde afstand ({len(recent_distances)} metingen): {average_distance / 1000:.2f} m")
            else:
                print(f"Geen valide metingen rond hoek {TARGET_ANGLE}°.")

            # Bereken hoek van de muur
            closest_points1 = find_closest_points(points, X_POSITIONS[0], num_points=5)
            closest_points2 = find_closest_points(points, X_POSITIONS[1], num_points=5)

            point1 = calculate_average_point(closest_points1)
            point2 = calculate_average_point(closest_points2)

            wall_angle = calculate_angle_between_points(point1, point2)

            # Filter foutieve metingen op hoek
            if wall_angle is not None and abs(wall_angle) <= MAX_ANGLE_THRESHOLD:
                recent_angles.append(wall_angle)
                if len(recent_angles) > NUM_MEASUREMENTS:
                    recent_angles.pop(0)
                average_angle = sum(recent_angles) / len(recent_angles)
                print(f"Gemiddelde muurhoek ({len(recent_angles)} metingen): {average_angle:.2f}°")
            elif wall_angle is not None:
                print(f"Foutieve hoekmeting genegeerd: {wall_angle:.2f}°")
            else:
                print("Niet genoeg data om de muurhoek te berekenen.")

            # Schoon buffer en slaap
            lidar.clean_input()

    except KeyboardInterrupt:
        print("Stoppen...")
    finally:
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    main()
