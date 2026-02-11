document.addEventListener("DOMContentLoaded", function () {

    const fairField = document.querySelector("#id_fair")?.closest(".form-row, .fieldBox, .form-group");
    const channelField = document.querySelector("#id_channel");
    console.log(channelField)
    const amountField = document.querySelector("#id_amount")?.closest(".form-row, .fieldBox, .form-group");
    const reasonField = document.querySelector("#id_reason")?.closest(".form-row, .fieldBox, .form-group");
    const productField = document.querySelector("#id_product")?.closest(".form-row, .fieldBox, .form-group");

    function toggleFields() {

        const fairValue = document.querySelector("#id_fair")?.value;
        const selectedChannelText = channelField?.selectedOptions[0]?.text?.toLowerCase();

        if (fairValue) {
            amountField?.style.setProperty("display", "none");
            reasonField?.style.setProperty("display", "none");
            productField?.style.setProperty("display", "none");
        } else {
            amountField?.style.removeProperty("display");
            reasonField?.style.removeProperty("display");
            productField?.style.removeProperty("display");
        }

        if (selectedChannelText && selectedChannelText.includes("digital")) {
            fairField?.style.setProperty("display", "none");
        } else {
            fairField?.style.removeProperty("display");
        }
    }

    document.querySelector("#id_fair")?.addEventListener("change", toggleFields);
    channelField?.addEventListener("change", toggleFields);

    toggleFields();
});
