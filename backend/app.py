from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

file_path = "../Uber_Ride_Booking_Analysis.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="ncr_ride_bookings"
)

# Clean column names
df.columns = df.columns.str.strip()


# ---------------------------------------------------
# BASIC DATA CLEANING
# ---------------------------------------------------

df["Booking Value"] = pd.to_numeric(
    df["Booking Value"],
    errors="coerce"
).fillna(0)

df["Ride Distance"] = pd.to_numeric(
    df["Ride Distance"],
    errors="coerce"
)

df["Driver Ratings"] = pd.to_numeric(
    df["Driver Ratings"],
    errors="coerce"
)

df["Customer Rating"] = pd.to_numeric(
    df["Customer Rating"],
    errors="coerce"
)

# Convert date
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# Convert time
df["Time"] = pd.to_datetime(
    df["Time"].astype(str),
    format="%H:%M:%S",
    errors="coerce"
)


# ---------------------------------------------------
# HOME ROUTE
# ---------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "Uber Ride Booking Analytics API is running!"
    })


# ---------------------------------------------------
# DASHBOARD API
# ---------------------------------------------------

@app.route("/api/dashboard")
def dashboard():

    # -----------------------------
    # KPI METRICS
    # -----------------------------

    total_bookings = len(df)

    total_revenue = df["Booking Value"].sum()

    completed_rides = (
        df["Booking Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("completed")
        .sum()
    )

    cancelled_customer = pd.to_numeric(
        df["Cancelled Rides by Customer"],
        errors="coerce"
    ).fillna(0)

    cancelled_driver = pd.to_numeric(
        df["Cancelled Rides by Driver"],
        errors="coerce"
    ).fillna(0)

    total_cancelled_customer = int(
        (cancelled_customer > 0).sum()
    )

    total_cancelled_driver = int(
        (cancelled_driver > 0).sum()
    )

    total_cancelled = (
        total_cancelled_customer
        + total_cancelled_driver
    )

    cancellation_rate = (
        total_cancelled / total_bookings * 100
        if total_bookings > 0
        else 0
    )

    completion_rate = (
        completed_rides / total_bookings * 100
        if total_bookings > 0
        else 0
    )

    average_revenue = (
        total_revenue / total_bookings
        if total_bookings > 0
        else 0
    )


    # ---------------------------------------------------
    # BOOKING STATUS
    # ---------------------------------------------------

    booking_status = (
        df["Booking Status"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    booking_status.columns = [
        "name",
        "value"
    ]

    booking_status_data = booking_status.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # VEHICLE BOOKINGS
    # ---------------------------------------------------

    vehicle_bookings = (
        df["Vehicle Type"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    vehicle_bookings.columns = [
        "name",
        "bookings"
    ]

    vehicle_bookings_data = vehicle_bookings.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # REVENUE BY VEHICLE
    # ---------------------------------------------------

    revenue_vehicle = (
        df.groupby("Vehicle Type")["Booking Value"]
        .sum()
        .reset_index()
    )

    revenue_vehicle.columns = [
        "name",
        "revenue"
    ]

    revenue_vehicle = revenue_vehicle.sort_values(
        "revenue",
        ascending=False
    )

    revenue_vehicle_data = revenue_vehicle.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # PAYMENT METHODS
    # ---------------------------------------------------

    payment_methods = (
        df["Payment Method"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    payment_methods.columns = [
        "name",
        "value"
    ]

    payment_methods_data = payment_methods.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # TOP PICKUP LOCATIONS
    # ---------------------------------------------------

    pickup_locations = (
        df["Pickup Location"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
        .reset_index()
    )

    pickup_locations.columns = [
        "name",
        "bookings"
    ]

    pickup_locations_data = pickup_locations.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # AVERAGE RIDE DISTANCE BY VEHICLE
    # ---------------------------------------------------

    distance_vehicle = (
        df.groupby("Vehicle Type")["Ride Distance"]
        .mean()
        .dropna()
        .reset_index()
    )

    distance_vehicle.columns = [
        "name",
        "distance"
    ]

    distance_vehicle_data = distance_vehicle.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # DRIVER RATINGS
    # ---------------------------------------------------

    driver_rating = (
        df.groupby("Vehicle Type")["Driver Ratings"]
        .mean()
        .dropna()
        .reset_index()
    )

    driver_rating.columns = [
        "name",
        "rating"
    ]

    driver_rating_data = driver_rating.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # CUSTOMER RATINGS
    # ---------------------------------------------------

    customer_rating = (
        df.groupby("Vehicle Type")["Customer Rating"]
        .mean()
        .dropna()
        .reset_index()
    )

    customer_rating.columns = [
        "name",
        "rating"
    ]

    customer_rating_data = customer_rating.to_dict(
        orient="records"
    )


    # ---------------------------------------------------
    # MONTHLY BOOKINGS
    # ---------------------------------------------------

    monthly_bookings = (
        df.dropna(subset=["Date"])
        .assign(
            Month=df["Date"].dt.strftime("%b")
        )
        .groupby(
            ["Month", df["Date"].dt.month]
        )
        .size()
        .reset_index(name="bookings")
        .sort_values("Date")
    )

    monthly_bookings_data = [
        {
            "name": row["Month"],
            "bookings": int(row["bookings"])
        }
        for _, row in monthly_bookings.iterrows()
    ]


    # ---------------------------------------------------
    # PEAK BOOKING HOURS
    # ---------------------------------------------------

    df["Hour"] = df["Time"].dt.hour

    hourly_bookings = (
        df.dropna(subset=["Hour"])
        .groupby("Hour")
        .size()
        .reset_index(name="bookings")
        .sort_values("Hour")
    )

    hourly_bookings_data = [
        {
            "hour": int(row["Hour"]),
            "bookings": int(row["bookings"])
        }
        for _, row in hourly_bookings.iterrows()
    ]


    # ---------------------------------------------------
    # FINAL API RESPONSE
    # ---------------------------------------------------

    return jsonify({

        # KPIs
        "totalBookings": int(total_bookings),
        "totalRevenue": float(total_revenue),
        "completedRides": int(completed_rides),
        "cancelledRides": int(total_cancelled),
        "cancellationRate": round(
            cancellation_rate,
            2
        ),
        "completionRate": round(
            completion_rate,
            2
        ),
        "averageRevenue": round(
            average_revenue,
            2
        ),

        # Charts
        "bookingStatus": booking_status_data,

        "vehicleBookings": vehicle_bookings_data,

        "revenueByVehicle": revenue_vehicle_data,

        "paymentMethods": payment_methods_data,

        "pickupLocations": pickup_locations_data,

        "rideDistance": distance_vehicle_data,

        "driverRatings": driver_rating_data,

        "customerRatings": customer_rating_data,

        "monthlyBookings": monthly_bookings_data,

        "hourlyBookings": hourly_bookings_data
    })


# ---------------------------------------------------
# RUN SERVER
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )