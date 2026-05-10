const LoadingScreen = () => {

    return (

        <div
            style={{
                display: "flex",

                justifyContent: "center",

                alignItems: "center",

                minHeight: "100vh",

                background: "#0f172a",

                color: "white",

                flexDirection: "column",
            }}
        >

            <div
                style={{
                    width: "60px",

                    height: "60px",

                    border:
                        "6px solid #1e293b",

                    borderTop:
                        "6px solid #3b82f6",

                    borderRadius: "50%",

                    animation:
                        "spin 1s linear infinite",
                }}
            />

            <h2
                style={{
                    marginTop: "20px",
                }}
            >
                Connecting to
                PredictaMaint...
            </h2>

            <p
                style={{
                    marginTop: "10px",
                    opacity: 0.7,
                }}
            >
                Initializing live
                industrial telemetry
            </p>

        </div>
    )
}

export default LoadingScreen