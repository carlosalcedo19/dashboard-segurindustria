(function() {
    const initDynamicFields = () => {
        const getRow = (id) => document.querySelector(id)?.closest(".unfold-form-row, .form-row, .fieldBox");

        const fairInput = document.querySelector("#id_fair");
        const channelField = document.querySelector("#id_channel");
        
        const fairRow = getRow("#id_fair");
        const amountRow = getRow("#id_amount");
        const reasonRow = getRow("#id_reason");
        const productRow = getRow("#id_product");

        function toggleFields() {
            const fairValue = fairInput?.value;
            const selectedChannelText = channelField?.selectedOptions[0]?.text?.toLowerCase() || "";

            if (fairValue && fairValue !== "") {
                if (amountRow) amountRow.style.display = "none";
                if (reasonRow) reasonRow.style.display = "none";
                if (productRow) productRow.style.display = "none";
            } else {
                if (amountRow) amountRow.style.display = "block";
                if (reasonRow) reasonRow.style.display = "block";
                if (productRow) productRow.style.display = "block";
            }

            if (selectedChannelText.includes("digital")) {
                if (fairRow) fairRow.style.display = "none";
            } else {
                if (fairRow) fairRow.style.display = "block";
            }
        }

        fairInput?.addEventListener("change", toggleFields);
        channelField?.addEventListener("change", toggleFields);

        toggleFields();
    };

    if (document.readyState === "complete" || document.readyState === "interactive") {
        initDynamicFields();
    } else {
        document.addEventListener("DOMContentLoaded", initDynamicFields);
    }
})();