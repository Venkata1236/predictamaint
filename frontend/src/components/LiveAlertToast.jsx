const LiveAlertToast = ({
    incident,
}) => {

    if (!incident) {
        return null
    }

    return (

        <div
            style={{
                position: "fixed",

                top: "20px",

                right: "20px",

                width: "320px",

                background: "#7f1d1d",

                border:
                    "2px solid #ef4444",

                padding: "20px",

                borderRadius: "16px",

                color: "white",

                zIndex: 9999,

                boxShadow:
                    "0 10px 30px rgba(0,0,0,0.4)",

                animation:
                    "pulseCritical 1.5s infinite",
            }}
        >

            <h3>
                Critical Incident
            </h3>

            <p
                style={{
                    marginTop: "10px",
                    opacity: 0.9,
                }}
            >
                Machine:
                {" "}
                {incident.machine_id}
            </p>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                AI detected abnormal
                industrial behavior.
            </p>

            <div
                style={{
                    marginTop: "16px",

                    display: "flex",

                    gap: "8px",

                    flexWrap: "wrap",
                }}
            >

                {
                    incident
                    .anomalous_features
                    .map((feature) => (

                        <div
                            key={feature}

                            style={{
                                background:
                                    "#111827",

                                padding:
                                    "6px 12px",

                                borderRadius:
                                    "999px",

                                fontSize:
                                    "13px",
                            }}
                        >
                            {feature}
                        </div>
                    ))
                }

            </div>

        </div>
    )
}

export default LiveAlertToast