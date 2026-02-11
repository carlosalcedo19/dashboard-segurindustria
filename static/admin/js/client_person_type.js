document.addEventListener("DOMContentLoaded", function () {

    const personType = document.querySelector("#id_person_type");

    function getFieldBlock(fieldId) {
        const input = document.querySelector(fieldId);
        if (!input) return null;

        return input.closest("[data-field]") ||
               input.closest(".form-row") ||
               input.closest(".field-box") ||
               input.closest(".mb-4") ||
               input.parentElement?.parentElement?.parentElement;
    }

    const companyField = getFieldBlock("#id_company");
    const positionField = getFieldBlock("#id_position");

    const documentTypeField = getFieldBlock("#id_document_type");
    const documentNumberField = getFieldBlock("#id_document_number");

    function toggleFields() {

        if (!personType) return;

        const isEmpresa = personType.value === "Empresa";

        if (companyField) companyField.style.display = isEmpresa ? "" : "none";
        if (positionField) positionField.style.display = isEmpresa ? "" : "none";

        if (documentTypeField) documentTypeField.style.display = isEmpresa ? "none" : "";
        if (documentNumberField) documentNumberField.style.display = isEmpresa ? "none" : "";
    }

    toggleFields();
    personType.addEventListener("change", toggleFields);

});
