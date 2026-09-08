import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# UBER RIDE BOOKING ANALYTICS
# ============================================================

print("=" * 70)
print("UBER RIDE BOOKING ANALYTICS")
print("=" * 70)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

file_path = "Uber_Ride_Booking_Analysis.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="ncr_ride_bookings"
)

print("\nData loaded successfully!")

# ------------------------------------------------------------
# 2. BASIC DATASET INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("1. DATASET INFORMATION")
print("=" * 70)

print("\nDataset Shape:")
print(df.shape)

print("\nNumber of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])

print("\nColumn Names:")
for column in df.columns:
    print("-", column)

# ------------------------------------------------------------
# 3. FIRST 5 ROWS
# ------------------------------------------------------------

print("\nFirst 5 Rows:")
print(df.head())

# ------------------------------------------------------------
# 4. MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("2. MISSING VALUES ANALYSIS")
print("=" * 70)

missing_values = df.isnull().sum()

print("\nMissing Values by Column:")
print(missing_values)

print("\nTotal Missing Values:", missing_values.sum())

# Columns having missing values
print("\nColumns with Missing Values:")
print(missing_values[missing_values > 0])

# ------------------------------------------------------------
# 5. DUPLICATE ROWS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("3. DUPLICATE ROW ANALYSIS")
print("=" * 70)

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_rows)

if duplicate_rows == 0:
    print("No completely duplicate rows found.")
else:
    print("Duplicate rows are present.")

# ------------------------------------------------------------
# 6. DATA TYPES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("4. DATA TYPES")
print("=" * 70)

print("\nColumn Data Types:")
print(df.dtypes)

# ------------------------------------------------------------
# 7. STATISTICAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("5. STATISTICAL SUMMARY")
print("=" * 70)

print("\nNumerical Statistics:")
print(df.describe())

# ------------------------------------------------------------
# 8. BOOKING STATUS ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("6. BOOKING STATUS ANALYSIS")
print("=" * 70)

booking_status = df["Booking Status"].value_counts()

print("\nBooking Status Count:")
print(booking_status)

print("\nBooking Status Percentage:")
print((booking_status / len(df) * 100).round(2))

# ------------------------------------------------------------
# 9. VEHICLE TYPE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("7. VEHICLE TYPE ANALYSIS")
print("=" * 70)

vehicle_bookings = df["Vehicle Type"].value_counts()

print("\nBookings by Vehicle Type:")
print(vehicle_bookings)

# ------------------------------------------------------------
# 10. REVENUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("8. REVENUE ANALYSIS")
print("=" * 70)

total_revenue = df["Booking Value"].sum()

print("\nTotal Booking Value:", total_revenue)

revenue_by_vehicle = (
    df.groupby("Vehicle Type")["Booking Value"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Vehicle Type:")
print(revenue_by_vehicle)

# ------------------------------------------------------------
# 11. CANCELLATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("9. CANCELLATION ANALYSIS")
print("=" * 70)

customer_cancellations = df[
    "Cancelled Rides by Customer"
].notna().sum()

driver_cancellations = df[
    "Cancelled Rides by Driver"
].notna().sum()

print("\nCustomer Cancellation Records:", customer_cancellations)
print("Driver Cancellation Records:", driver_cancellations)

total_cancellations = (
    customer_cancellations +
    driver_cancellations
)

cancellation_rate = (
    total_cancellations / len(df)
) * 100

print("\nTotal Cancellation Records:", total_cancellations)
print("Cancellation Rate:", round(cancellation_rate, 2), "%")

# ------------------------------------------------------------
# 12. CUSTOMER CANCELLATION REASONS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("10. CUSTOMER CANCELLATION REASONS")
print("=" * 70)

customer_cancel_reasons = (
    df["Reason for cancelling by Customer"]
    .value_counts()
)

print("\nTop Customer Cancellation Reasons:")
print(customer_cancel_reasons.head(10))

# ------------------------------------------------------------
# 13. DRIVER CANCELLATION REASONS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("11. DRIVER CANCELLATION REASONS")
print("=" * 70)

driver_cancel_reasons = (
    df["Driver Cancellation Reason"]
    .value_counts()
)

print("\nTop Driver Cancellation Reasons:")
print(driver_cancel_reasons.head(10))

# ------------------------------------------------------------
# 14. PAYMENT METHOD ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("12. PAYMENT METHOD ANALYSIS")
print("=" * 70)

payment_methods = df["Payment Method"].value_counts()

print("\nPayment Method Usage:")
print(payment_methods)

print("\nPayment Method Percentage:")
print(
    (payment_methods / payment_methods.sum() * 100)
    .round(2)
)

# ------------------------------------------------------------
# 15. PICKUP LOCATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("13. PICKUP LOCATION ANALYSIS")
print("=" * 70)

pickup_locations = df["Pickup Location"].value_counts()

print("\nTop 10 Pickup Locations:")
print(pickup_locations.head(10))

# ------------------------------------------------------------
# 16. DROP LOCATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("14. DROP LOCATION ANALYSIS")
print("=" * 70)

drop_locations = df["Drop Location"].value_counts()

print("\nTop 10 Drop Locations:")
print(drop_locations.head(10))

# ------------------------------------------------------------
# 17. RIDE DISTANCE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("15. RIDE DISTANCE ANALYSIS")
print("=" * 70)

print("\nOverall Ride Distance Statistics:")
print(df["Ride Distance"].describe())

average_distance = df["Ride Distance"].mean()

print(
    "\nAverage Ride Distance:",
    round(average_distance, 2)
)

distance_by_vehicle = (
    df.groupby("Vehicle Type")["Ride Distance"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Ride Distance by Vehicle Type:")
print(distance_by_vehicle.round(2))

# ------------------------------------------------------------
# 18. DRIVER RATING ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("16. DRIVER RATING ANALYSIS")
print("=" * 70)

average_driver_rating = df["Driver Ratings"].mean()

print(
    "\nOverall Average Driver Rating:",
    round(average_driver_rating, 2)
)

driver_rating_by_vehicle = (
    df.groupby("Vehicle Type")["Driver Ratings"]
    .mean()
    .sort_values(ascending=False)
)

print("\nDriver Rating by Vehicle Type:")
print(driver_rating_by_vehicle.round(2))

# ------------------------------------------------------------
# 19. CUSTOMER RATING ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("17. CUSTOMER RATING ANALYSIS")
print("=" * 70)

average_customer_rating = df["Customer Rating"].mean()

print(
    "\nOverall Average Customer Rating:",
    round(average_customer_rating, 2)
)

customer_rating_by_vehicle = (
    df.groupby("Vehicle Type")["Customer Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("\nCustomer Rating by Vehicle Type:")
print(customer_rating_by_vehicle.round(2))

# ------------------------------------------------------------
# 20. BOOKING VALUE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("18. BOOKING VALUE ANALYSIS")
print("=" * 70)

print("\nBooking Value Statistics:")
print(df["Booking Value"].describe())

average_booking_value = df["Booking Value"].mean()

print(
    "\nAverage Booking Value:",
    round(average_booking_value, 2)
)

# ------------------------------------------------------------
# 21. DATE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("19. DATE ANALYSIS")
print("=" * 70)

df["Date"] = pd.to_datetime(df["Date"])

print("\nDate Range:")
print("Start Date:", df["Date"].min())
print("End Date:", df["Date"].max())

daily_bookings = df["Date"].value_counts().sort_index()

print("\nTop 10 Dates by Booking Volume:")
print(daily_bookings.sort_values(ascending=False).head(10))

# ------------------------------------------------------------
# 22. MONTHLY BOOKING ANALYSIS
# ------------------------------------------------------------

monthly_bookings = (
    df.groupby(df["Date"].dt.month)["Booking ID"]
    .count()
)

print("\nBookings by Month:")
print(monthly_bookings)

# ------------------------------------------------------------
# 23. HOURLY ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("20. TIME ANALYSIS")
print("=" * 70)

df["Time"] = pd.to_datetime(
    df["Time"],
    format="%H:%M:%S"
)

hourly_bookings = (
    df.groupby(df["Time"].dt.hour)["Booking ID"]
    .count()
)

print("\nBookings by Hour:")
print(hourly_bookings)

peak_hour = hourly_bookings.idxmax()
peak_hour_bookings = hourly_bookings.max()

print(
    "\nPeak Booking Hour:",
    peak_hour,
    "with",
    peak_hour_bookings,
    "bookings"
)

# ------------------------------------------------------------
# 24. COMPLETED RIDE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("21. COMPLETED RIDE ANALYSIS")
print("=" * 70)

completed_rides = df[
    df["Booking Status"] == "Completed"
]

print("\nCompleted Rides:", len(completed_rides))

completed_revenue = completed_rides["Booking Value"].sum()

print(
    "Revenue from Completed Rides:",
    completed_revenue
)

completed_distance = completed_rides["Ride Distance"].mean()

print(
    "Average Distance of Completed Rides:",
    round(completed_distance, 2)
)

# ------------------------------------------------------------
# 25. BUSINESS INSIGHTS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("22. KEY BUSINESS INSIGHTS")
print("=" * 70)

most_used_vehicle = vehicle_bookings.idxmax()

top_pickup_location = pickup_locations.idxmax()

top_payment_method = payment_methods.idxmax()

highest_revenue_vehicle = revenue_by_vehicle.idxmax()

longest_distance_vehicle = distance_by_vehicle.idxmax()

highest_driver_rating_vehicle = driver_rating_by_vehicle.idxmax()

highest_customer_rating_vehicle = customer_rating_by_vehicle.idxmax()

print("\n1. Most Used Vehicle Type:")
print(most_used_vehicle)

print("\n2. Highest Revenue Vehicle Type:")
print(highest_revenue_vehicle)

print("\n3. Top Pickup Location:")
print(top_pickup_location)

print("\n4. Most Used Payment Method:")
print(top_payment_method)

print("\n5. Vehicle Type with Highest Average Ride Distance:")
print(longest_distance_vehicle)

print("\n6. Vehicle Type with Highest Driver Rating:")
print(highest_driver_rating_vehicle)

print("\n7. Vehicle Type with Highest Customer Rating:")
print(highest_customer_rating_vehicle)

# ------------------------------------------------------------
# 26. VISUALIZATIONS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("23. GENERATING VISUALIZATIONS")
print("=" * 70)

# Chart 1: Booking Status
plt.figure(figsize=(8, 6))

booking_status.plot(
    kind="bar"
)

plt.title("Booking Status Distribution")
plt.xlabel("Booking Status")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 2: Vehicle Bookings
plt.figure(figsize=(10, 6))

vehicle_bookings.plot(
    kind="bar"
)

plt.title("Bookings by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 3: Revenue by Vehicle
plt.figure(figsize=(10, 6))

revenue_by_vehicle.plot(
    kind="bar"
)

plt.title("Revenue by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 4: Top Pickup Locations
plt.figure(figsize=(10, 6))

pickup_locations.head(10).sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Pickup Locations")
plt.xlabel("Number of Bookings")
plt.ylabel("Pickup Location")
plt.tight_layout()
plt.show()

# Chart 5: Average Ride Distance
plt.figure(figsize=(10, 6))

distance_by_vehicle.plot(
    kind="bar"
)

plt.title("Average Ride Distance by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Distance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 6: Driver Ratings
plt.figure(figsize=(10, 6))

driver_rating_by_vehicle.plot(
    kind="bar"
)

plt.title("Average Driver Rating by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Driver Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 7: Customer Ratings
plt.figure(figsize=(10, 6))

customer_rating_by_vehicle.plot(
    kind="bar"
)

plt.title("Average Customer Rating by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Customer Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 8: Bookings by Hour
plt.figure(figsize=(10, 6))

hourly_bookings.plot(
    kind="line",
    marker="o"
)

plt.title("Bookings by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Number of Bookings")
plt.grid(True)
plt.tight_layout()
plt.show()

# Chart 9: Bookings by Month
plt.figure(figsize=(10, 6))

monthly_bookings.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Booking Trend")
plt.xlabel("Month")
plt.ylabel("Number of Bookings")
plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 27. FINAL MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nPython analysis covered:")
print("- Data Quality")
print("- Missing Values")
print("- Duplicate Analysis")
print("- Data Types")
print("- Statistical Analysis")
print("- Booking Analysis")
print("- Vehicle Analysis")
print("- Revenue Analysis")
print("- Cancellation Analysis")
print("- Payment Analysis")
print("- Location Analysis")
print("- Ride Distance Analysis")
print("- Rating Analysis")
print("- Date & Time Analysis")
print("- Business Insights")
print("- Data Visualization")

print("\nUber Ride Booking Analytics completed!")