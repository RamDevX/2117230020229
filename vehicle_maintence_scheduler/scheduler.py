from api_client import fetch_depot, fetch_vehicles


def get_duration(vehicle):
    return int(vehicle["Duration"])


def get_impact(vehicle):
    return int(vehicle["Impact"])


def get_task_id(vehicle):
    return vehicle["TaskID"]


def get_mechanic_hours(depot_data):
    depots = depot_data.get("depots", [])

    if not depots:
        raise ValueError("No depots found in response")

    best_depot = max(depots, key=lambda d: d["MechanicHours"])
    return int(best_depot["MechanicHours"])


def select_tasks(vehicles, max_hours):
    n = len(vehicles)

    dp = [[0 for _ in range(max_hours + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        vehicle = vehicles[i - 1]
        duration = get_duration(vehicle)
        impact = get_impact(vehicle)

        for h in range(max_hours + 1):
            if duration <= h:
                dp[i][h] = max(
                    impact + dp[i - 1][h - duration],
                    dp[i - 1][h]
                )
            else:
                dp[i][h] = dp[i - 1][h]

    selected = []
    h = max_hours

    for i in range(n, 0, -1):
        if dp[i][h] != dp[i - 1][h]:
            vehicle = vehicles[i - 1]
            selected.append(vehicle)
            h -= get_duration(vehicle)

    selected.reverse()
    return selected, dp[n][max_hours]


def main():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJyYW1wcmFrYXNoMjMxMDA1QGdtYWlsLmNvbSIsImV4cCI6MTc3ODA0OTIzNCwiaWF0IjoxNzc4MDQ4MzM0LCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiZWU1OTYwOGItN2E0OC00ZGYwLWI1ZmYtZTI4MWFmMzZkYmY3IiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoic3VicmFtYW5pYW4gcmFtcHJha2FzaCIsInN1YiI6IjJhYzU3YzBmLTRmZDktNGRjZC1iZTU5LTdlYzBiYzdmNjliOCJ9LCJlbWFpbCI6InJhbXByYWthc2gyMzEwMDVAZ21haWwuY29tIiwibmFtZSI6InN1YnJhbWFuaWFuIHJhbXByYWthc2giLCJyb2xsTm8iOiIyMTE3MjMwMDIwMjI5IiwiYWNjZXNzQ29kZSI6IkJUQ0RxVCIsImNsaWVudElEIjoiMmFjNTdjMGYtNGZkOS00ZGNkLWJlNTktN2VjMGJjN2Y2OWI4IiwiY2xpZW50U2VjcmV0IjoiWUZ6QmpGZ2tEVkdmRXNjaCJ9.h38C0B41LN0ZtTg-DhXmh4ETemFwwoPZy-7BRQNaCzE"

    depot_data = fetch_depot(token)
    vehicle_data = fetch_vehicles(token)

    print("\nDepot Response:", depot_data)
    print("\nVehicle Sample:", vehicle_data["vehicles"][0])

    mechanic_hours = get_mechanic_hours(depot_data)
    vehicles = vehicle_data["vehicles"]

    print("\nMechanic Hours:", mechanic_hours)
    print("Total Vehicles:", len(vehicles))

    selected, total_impact = select_tasks(vehicles, mechanic_hours)

    print("\nSelected Vehicles:")
    for v in selected:
        print(
            f"ID: {get_task_id(v)}, "
            f"Duration: {get_duration(v)}, "
            f"Impact: {get_impact(v)}"
        )

    print("\nTotal Impact:", total_impact)


if __name__ == "__main__":
    main()