const Sidebar = () => {

    const menuItems = [

        "Dashboard",

        "Incidents",

        "Diagnostics",

        "Maintenance",

        "Settings",
    ]

    return (

        <div
            style={{
                width:
                    window.innerWidth < 1000
                    ? "100%"
                    : "260px",

                background: "#111827",

                minHeight: "100vh",

                padding: "24px",

                borderRight:
                    "1px solid #1e293b",
            }}
        >

            <h1
                style={{
                    marginBottom: "40px",
                    fontSize: "28px",
                }}
            >
                PredictaMaint
            </h1>

            <div
                style={{
                    display: "flex",
                    flexDirection:
                        "column",

                    gap: "12px",
                }}
            >

                {
                    menuItems.map(
                        (item) => (

                        <div
                            key={item}

                            style={{
                                padding:
                                    "14px 18px",

                                borderRadius:
                                    "12px",

                                background:
                                    item ===
                                    "Dashboard"
                                    ? "#1e293b"
                                    : "transparent",

                                cursor:
                                    "pointer",

                                transition:
                                    "0.2s ease",
                            }}
                        >
                            {item}
                        </div>
                    ))
                }

            </div>

        </div>
    )
}

export default Sidebar