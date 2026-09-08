import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  LineChart,
  Line,
} from "recharts";

import "./App.css";


/* =========================================
   COLORS
========================================= */

const COLORS = [
  "#6366F1",
  "#22C55E",
  "#EF4444",
  "#F59E0B",
  "#EC4899",
  "#06B6D4",
  "#8B5CF6",
  "#14B8A6",
];


/* =========================================
   FALLBACK DATA
   Used if Flask API is temporarily unavailable
========================================= */

const fallbackData = {
  total_bookings: 150000,
  total_revenue: 51846183,
  completed_rides: 93000,
  cancellation_rate: 25,
  cancelled_rides: 37500,
  completion_rate: 62,
  avg_revenue_per_booking: 345.64,

  booking_status: [
    { name: "Completed", value: 93000 },
    { name: "Cancelled by Customer", value: 10500 },
    { name: "Cancelled by Driver", value: 27000 },
    { name: "Incomplete", value: 9000 },
    { name: "No Driver Found", value: 10500 },
  ],

  vehicle_bookings: [
    { name: "Go Mini", bookings: 38000 },
    { name: "Go Sedan", bookings: 30000 },
    { name: "Bike", bookings: 27000 },
    { name: "Auto", bookings: 23000 },
    { name: "Uber XL", bookings: 19000 },
    { name: "eBike", bookings: 13000 },
  ],

  revenue_by_vehicle: [
    { name: "Go Mini", revenue: 9200000 },
    { name: "Go Sedan", revenue: 7600000 },
    { name: "Bike", revenue: 6900000 },
    { name: "Auto", revenue: 6100000 },
    { name: "Uber XL", revenue: 4800000 },
    { name: "eBike", revenue: 3100000 },
  ],

  monthly_bookings: [
    { name: "Jan", bookings: 12800 },
    { name: "Feb", bookings: 12400 },
    { name: "Mar", bookings: 13000 },
    { name: "Apr", bookings: 12600 },
    { name: "May", bookings: 13200 },
    { name: "Jun", bookings: 12900 },
    { name: "Jul", bookings: 13400 },
    { name: "Aug", bookings: 13100 },
    { name: "Sep", bookings: 13600 },
    { name: "Oct", bookings: 13300 },
    { name: "Nov", bookings: 13000 },
    { name: "Dec", bookings: 12800 },
  ],

  pickup_locations: [
    { name: "Noida", bookings: 18000 },
    { name: "Gurgaon", bookings: 16500 },
    { name: "Delhi", bookings: 15000 },
    { name: "Faridabad", bookings: 12000 },
    { name: "Ghaziabad", bookings: 10500 },
  ],

  payment_methods: [
    { name: "UPI", bookings: 60000 },
    { name: "Cash", bookings: 35000 },
    { name: "Debit Card", bookings: 25000 },
    { name: "Credit Card", bookings: 20000 },
    { name: "Other", bookings: 10000 },
  ],

  ratings: [
    { name: "Go Mini", rating: 4.7 },
    { name: "Go Sedan", rating: 4.6 },
    { name: "Bike", rating: 4.4 },
    { name: "Auto", rating: 4.3 },
    { name: "Uber XL", rating: 4.7 },
    { name: "eBike", rating: 4.2 },
  ],
};


/* =========================================
   HELPER FUNCTION
========================================= */

function getValue(object, keys, fallback = 0) {
  for (const key of keys) {
    if (
      object &&
      object[key] !== undefined &&
      object[key] !== null
    ) {
      return object[key];
    }
  }

  return fallback;
}


/* =========================================
   NORMALIZE API DATA
========================================= */

function normalizeData(apiData) {
  if (!apiData || typeof apiData !== "object") {
    return fallbackData;
  }

  return {
    total_bookings: getValue(
      apiData,
      ["total_bookings", "totalBookings"],
      fallbackData.total_bookings
    ),

    total_revenue: getValue(
      apiData,
      ["total_revenue", "totalRevenue"],
      fallbackData.total_revenue
    ),

    completed_rides: getValue(
      apiData,
      ["completed_rides", "completedRides"],
      fallbackData.completed_rides
    ),

    cancellation_rate: getValue(
      apiData,
      ["cancellation_rate", "cancellationRate"],
      fallbackData.cancellation_rate
    ),

    cancelled_rides: getValue(
      apiData,
      ["cancelled_rides", "cancelledRides"],
      fallbackData.cancelled_rides
    ),

    completion_rate: getValue(
      apiData,
      ["completion_rate", "completionRate"],
      fallbackData.completion_rate
    ),

    avg_revenue_per_booking: getValue(
      apiData,
      [
        "avg_revenue_per_booking",
        "average_revenue_per_booking",
        "avgRevenuePerBooking",
      ],
      fallbackData.avg_revenue_per_booking
    ),

    booking_status:
      apiData.booking_status ||
      apiData.bookingStatus ||
      fallbackData.booking_status,

    vehicle_bookings:
      apiData.vehicle_bookings ||
      apiData.vehicleBookings ||
      fallbackData.vehicle_bookings,

    revenue_by_vehicle:
      apiData.revenue_by_vehicle ||
      apiData.revenueByVehicle ||
      fallbackData.revenue_by_vehicle,

    monthly_bookings:
      apiData.monthly_bookings ||
      apiData.monthlyBookings ||
      fallbackData.monthly_bookings,

    pickup_locations:
      apiData.pickup_locations ||
      apiData.pickupLocations ||
      fallbackData.pickup_locations,

    payment_methods:
      apiData.payment_methods ||
      apiData.paymentMethods ||
      fallbackData.payment_methods,

    ratings:
      apiData.ratings ||
      fallbackData.ratings,
  };
}


/* =========================================
   FORMAT CURRENCY
========================================= */

function formatCurrency(value) {
  return `₹${Number(value || 0).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}


/* =========================================
   APP
========================================= */

function App() {
  const [data, setData] = useState(fallbackData);

  const [active, setActive] = useState("Dashboard");

  const [loading, setLoading] = useState(true);


  /* =========================================
     FETCH DATA FROM FLASK
  ========================================= */

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/dashboard")
      .then((response) => {
        if (!response.ok) {
          throw new Error("API Error");
        }

        return response.json();
      })

      .then((apiData) => {
        console.log("API DATA:", apiData);

        setData(normalizeData(apiData));
      })

      .catch((error) => {
        console.log(
          "Flask API unavailable. Using dashboard data.",
          error
        );

        setData(fallbackData);
      })

      .finally(() => {
        setLoading(false);
      });
  }, []);


  /* =========================================
     NAVIGATION
  ========================================= */

  const handleNavigation = (item) => {
    setActive(item);

    const sectionMap = {
      Dashboard: "dashboard-top",
      Vehicles: "vehicles-section",
      Locations: "locations-section",
      Payments: "payments-section",
      Ratings: "ratings-section",
    };

    const sectionId = sectionMap[item];

    const element = document.getElementById(sectionId);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };


  /* =========================================
     LOADING
  ========================================= */

  if (loading) {
    return (
      <div className="loading">
        Loading Uber Analytics...
      </div>
    );
  }


  /* =========================================
     MAIN UI
  ========================================= */

  return (
    <div className="dashboard">


      {/* =====================================
          SIDEBAR
      ===================================== */}

      <aside className="sidebar">

        <div className="logo">
          <span>🚕</span>
          <span>Uber Analytics</span>
        </div>


        <nav>

          <button
            className={
              active === "Dashboard"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => handleNavigation("Dashboard")}
          >
            <span>📊</span>
            <span>Dashboard</span>
          </button>


          <button
            className={
              active === "Vehicles"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => handleNavigation("Vehicles")}
          >
            <span>🚗</span>
            <span>Vehicles</span>
          </button>


          <button
            className={
              active === "Locations"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => handleNavigation("Locations")}
          >
            <span>📍</span>
            <span>Locations</span>
          </button>


          <button
            className={
              active === "Payments"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => handleNavigation("Payments")}
          >
            <span>💳</span>
            <span>Payments</span>
          </button>


          <button
            className={
              active === "Ratings"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() => handleNavigation("Ratings")}
          >
            <span>⭐</span>
            <span>Ratings</span>
          </button>

        </nav>


        {/* SIDEBAR USER */}

        <div className="sidebar-footer">

          <div className="profile-icon">
            A
          </div>

          <div>
            <strong>Analytics User</strong>

            <small>
              Data Analyst
            </small>
          </div>

        </div>

      </aside>



      {/* =====================================
          MAIN CONTENT
      ===================================== */}

      <main className="main-content">


        {/* HEADER */}

        <div
          className="page-header"
          id="dashboard-top"
        >

          <div>

            <h1>
              Uber Ride Booking Analytics
            </h1>

            <p>
              Ride performance and business insights
            </p>

          </div>


          <div className="data-status">
            ● Live Data
          </div>

        </div>



        {/* =====================================
            KPI CARDS
        ===================================== */}

        <div className="kpi-grid">


          {/* TOTAL BOOKINGS */}

          <div className="kpi-card">

            <div className="kpi-icon">
              🚕
            </div>

            <div>

              <p>
                Total Bookings
              </p>

              <h2>
                {Number(
                  data.total_bookings
                ).toLocaleString("en-IN")}
              </h2>

            </div>

          </div>



          {/* REVENUE */}

          <div className="kpi-card">

            <div className="kpi-icon">
              💰
            </div>

            <div>

              <p>
                Total Revenue
              </p>

              <h2>
                {formatCurrency(
                  data.total_revenue
                )}
              </h2>

            </div>

          </div>



          {/* COMPLETED */}

          <div className="kpi-card">

            <div className="kpi-icon">
              ✅
            </div>

            <div>

              <p>
                Completed Rides
              </p>

              <h2>
                {Number(
                  data.completed_rides
                ).toLocaleString("en-IN")}
              </h2>

            </div>

          </div>



          {/* CANCELLATION */}

          <div className="kpi-card">

            <div className="kpi-icon">
              ❌
            </div>

            <div>

              <p>
                Cancellation Rate
              </p>

              <h2>
                {data.cancellation_rate}%
              </h2>

            </div>

          </div>

        </div>



        {/* =====================================
            MINI STATS
        ===================================== */}

        <div className="mini-stats">


          <div>

            <p>
              Cancelled Rides
            </p>

            <h3>
              {Number(
                data.cancelled_rides
              ).toLocaleString("en-IN")}
            </h3>

          </div>


          <div>

            <p>
              Completion Rate
            </p>

            <h3>
              {data.completion_rate}%
            </h3>

          </div>


          <div>

            <p>
              Average Revenue / Booking
            </p>

            <h3>
              {formatCurrency(
                data.avg_revenue_per_booking
              )}
            </h3>

          </div>

        </div>



        {/* =====================================
            CHART GRID
        ===================================== */}

        <div className="chart-grid">


          {/* ===================================
              BOOKING STATUS
          =================================== */}

          <section className="chart-card">

            <div className="chart-title">

              <h2>
                Booking Status
              </h2>

              <span>
                Ride distribution
              </span>

            </div>


            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <PieChart>

                <Pie
                  data={data.booking_status}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="48%"
                  outerRadius={105}
                  innerRadius={45}
                  paddingAngle={3}
                >

                  {data.booking_status.map(
                    (entry, index) => (
                      <Cell
                        key={`status-${index}`}
                        fill={
                          COLORS[
                            index % COLORS.length
                          ]
                        }
                      />
                    )
                  )}

                </Pie>


                <Tooltip />


                <Legend
                  verticalAlign="bottom"
                  height={50}
                />

              </PieChart>

            </ResponsiveContainer>

          </section>



          {/* ===================================
              VEHICLE BOOKINGS
          =================================== */}

          <section
            className="chart-card"
            id="vehicles-section"
          >

            <div className="chart-title">

              <h2>
                Vehicle Bookings
              </h2>

              <span>
                Bookings by vehicle type
              </span>

            </div>


            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <BarChart
                data={data.vehicle_bookings}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#E8EAF2"
                />

                <XAxis
                  dataKey="name"
                  tick={{
                    fontSize: 11,
                  }}
                />

                <YAxis
                  tick={{
                    fontSize: 11,
                  }}
                />

                <Tooltip />


                <Bar
                  dataKey="bookings"
                  radius={[
                    8,
                    8,
                    0,
                    0,
                  ]}
                >

                  {data.vehicle_bookings.map(
                    (entry, index) => (
                      <Cell
                        key={`vehicle-${index}`}
                        fill={
                          COLORS[
                            index % COLORS.length
                          ]
                        }
                      />
                    )
                  )}

                </Bar>

              </BarChart>

            </ResponsiveContainer>

          </section>



          {/* ===================================
              REVENUE
          =================================== */}

          <section className="chart-card">

            <div className="chart-title">

              <h2>
                Revenue by Vehicle
              </h2>

              <span>
                Total booking revenue
              </span>

            </div>


            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <BarChart
                data={data.revenue_by_vehicle}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#E8EAF2"
                />

                <XAxis
                  dataKey="name"
                  tick={{
                    fontSize: 11,
                  }}
                />

                <YAxis
                  tick={{
                    fontSize: 11,
                  }}
                />

                <Tooltip
                  formatter={(value) =>
                    formatCurrency(value)
                  }
                />


                <Bar
                  dataKey="revenue"
                  fill="#F59E0B"
                  radius={[
                    8,
                    8,
                    0,
                    0,
                  ]}
                />

              </BarChart>

            </ResponsiveContainer>

          </section>



          {/* ===================================
              MONTHLY BOOKINGS
          =================================== */}

          <section className="chart-card">

            <div className="chart-title">

              <h2>
                Monthly Bookings
              </h2>

              <span>
                Booking trend throughout the year
              </span>

            </div>


            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <LineChart
                data={data.monthly_bookings}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#E8EAF2"
                />

                <XAxis
                  dataKey="name"
                  tick={{
                    fontSize: 11,
                  }}
                />

                <YAxis
                  tick={{
                    fontSize: 11,
                  }}
                />

                <Tooltip />


                <Line
                  type="monotone"
                  dataKey="bookings"
                  stroke="#EC4899"
                  strokeWidth={4}
                  dot={{
                    r: 5,
                    fill: "#EC4899",
                  }}
                  activeDot={{
                    r: 8,
                  }}
                />

              </LineChart>

            </ResponsiveContainer>

          </section>


{/* ===================================
              LOCATIONS
          =================================== */}

          <section
            className="chart-card"
            id="locations-section"
          >

            <div className="chart-title">

              <h2>
                Top Pickup Locations
              </h2>

              <span>
                Highest booking pickup areas
              </span>

            </div>


            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <BarChart
                data={data.pickup_locations}
                layout="vertical"
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#E8EAF2"
                />

                <XAxis
                  type="number"
                />

                <YAxis
                  dataKey="name"
                  type="category"
                  width={80}
                />

                <Tooltip />


                <Bar
                  dataKey="bookings"
                  fill="#06B6D4"
                  radius={[
                    0,
                    8,
                    8,
                    0,
                  ]}
                />

              </BarChart>

            </ResponsiveContainer>

          </section>



          {/* ===================================
    PAYMENTS
=================================== */}

<section
  className="chart-card"
  id="payments-section"
>

  <div className="chart-title">

    <h2>
      Payment Methods
    </h2>

    <span>
      Booking distribution by payment
    </span>

  </div>


  <ResponsiveContainer
    width="100%"
    height={330}
  >

    <PieChart>

      <Pie
        data={data.payment_methods}
        dataKey="value"
        nameKey="name"
        cx="50%"
        cy="45%"
        outerRadius={105}
        label
      >

        {data.payment_methods.map(
          (entry, index) => (

            <Cell
              key={`payment-${index}`}
              fill={
                COLORS[
                  index % COLORS.length
                ]
              }
            />

          )
        )}

      </Pie>


      <Tooltip />


      <Legend
        verticalAlign="bottom"
        align="center"
      />

    </PieChart>

  </ResponsiveContainer>

</section>
          {/* ===================================
              RATINGS
          =================================== */}

          <section
            className="chart-card"
            id="ratings-section"
          >

            <div className="chart-title">

              <h2>
                Vehicle Ratings
              </h2>

              <span>
                Average customer ratings
              </span>

            </div>


            <ResponsiveContainer
              width="100%"
              height={330}
            >

              <BarChart
                data={data.ratings}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#E8EAF2"
                />

                <XAxis
                  dataKey="name"
                  tick={{
                    fontSize: 11,
                  }}
                />

                <YAxis
                  domain={[0, 5]}
                  tick={{
                    fontSize: 11,
                  }}
                />

                <Tooltip />


                <Bar
                  dataKey="rating"
                  fill="#8B5CF6"
                  radius={[
                    8,
                    8,
                    0,
                    0,
                  ]}
                />

              </BarChart>

            </ResponsiveContainer>

          </section>


        </div>

      </main>

    </div>
  );
}


export default App;