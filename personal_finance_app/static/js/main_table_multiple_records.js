$(document).ready(function() {
    // Function to load payment methods for a specific row and return a promise
    function loadPaymentMethodsForRow(row) {
        var user_id = row.find('.user_id').val();
        var paymentDropdown = row.find('.payment_method_id');

        return new Promise(function(resolve) {
            if (user_id) {
                $.ajax({
                    url: '/main_table/get_payment_methods/' + user_id,
                    type: 'GET',
                    success: function(data) {
                        paymentDropdown.empty();
                        paymentDropdown.append('<option value="">--Select Payment Method--</option>');
                        $.each(data.payment_methods, function(key, value) {
                            paymentDropdown.append('<option value="' + value.payment_method_id + '">' + value.method_name + '</option>');
                        });
                        resolve(); // Resolve after the payment methods are loaded
                    }
                });
            } else {
                paymentDropdown.empty();
                paymentDropdown.append('<option value="">--Select Payment Method--</option>');
                resolve(); // Resolve immediately if no user selected
            }
        });
    }

    // Function to load sub-categories for a specific row and return a promise
    function loadSubCategoriesForRow(row) {
        var category_id = row.find('.category_id').val();
        var subCategoryDropdown = row.find('.sub_category_id');

        return new Promise(function(resolve) {
            if (category_id) {
                $.ajax({
                    url: '/main_table/get_sub_categories/' + category_id,
                    type: 'GET',
                    success: function(data) {
                        subCategoryDropdown.empty();
                        subCategoryDropdown.append('<option value="">--Select Sub-Category--</option>');
                        $.each(data.sub_categories, function(key, value) {
                            subCategoryDropdown.append('<option value="' + value.sub_category_id + '">' + value.sub_category_name + '</option>');
                        });
                        resolve(); // Resolve after sub-categories are loaded
                    }
                });
            } else {
                subCategoryDropdown.empty();
                subCategoryDropdown.append('<option value="">--Select Sub-Category--</option>');
                resolve(); // Resolve immediately if no category selected
            }
        });
    }

    // Event delegation for user_id change in any row
    $(document).on('change', '.user_id', function() {
        var row = $(this).closest('.record-row'); // Get the closest row
        loadPaymentMethodsForRow(row); // Update the payment methods for that specific row
    });

    // Event delegation for category_id change in any row
    $(document).on('change', '.category_id', function() {
        var row = $(this).closest('.record-row'); // Get the closest row
        loadSubCategoriesForRow(row); // Update the sub-categories for that specific row
    });

    // Add functionality to dynamically add new rows
    $('#addRow').click(function() {
        var newRow = $('.record-row:first').clone();
        newRow.find('input').val(''); // Clear inputs
        newRow.find('.payment_method_id').empty().append('<option value="">--Select Payment Method--</option>'); // Clear payment method dropdown
        newRow.find('.sub_category_id').empty().append('<option value="">--Select Sub-Category--</option>'); // Clear sub-category dropdown
        $('#record-table tbody').append(newRow); // Append the new row
    });

    // Function to map text to dropdowns
    function mapTextToDropdown(selectElement, textValue) {
        selectElement.find('option').each(function() {
            if ($(this).text() === textValue) {
                $(this).prop('selected', true);
            }
        });
    }

    // Function to handle Excel-like data pasting
    $('#pasteBtn').click(function() {
        var pastedData = $('#excelInput').val().trim().split('\n');
        var headers = pastedData[0].split('\t');

        // Process each row, skipping the header
        pastedData.slice(1).forEach(function(row, index) {
            var rowData = row.split('\t');

            // Add a new row if necessary
            if (index > $('.record-row').length - 1) {
                $('#addRow').trigger('click');
            }

            var formRow = $('.record-row').eq(index);

            // Map text values to dropdowns (User, Category, Sub Category)
            mapTextToDropdown(formRow.find('select[name="user_id[]"]'), rowData[0]);
            mapTextToDropdown(formRow.find('select[name="category_id[]"]'), rowData[1]);

            // Load sub-categories after category is selected
            loadSubCategoriesForRow(formRow).then(function() {
                mapTextToDropdown(formRow.find('select[name="sub_category_id[]"]'), rowData[2]);
            });

            // Load payment methods after user is selected
            loadPaymentMethodsForRow(formRow).then(function() {
                mapTextToDropdown(formRow.find('select[name="payment_method_id[]"]'), rowData[3]);
            });

            // Fill in the remaining input fields
            formRow.find('input[name="year[]"]').val(rowData[4]);
            formRow.find('input[name="month[]"]').val(rowData[5]);
            formRow.find('input[name="day[]"]').val(rowData[6]);
            formRow.find('input[name="value[]"]').val(rowData[7]);
            formRow.find('input[name="description[]"]').val(rowData[8]);
        });
    });

    // Load payment methods and sub-categories for the first row if user and category are already selected
    $('.record-row').each(function() {
        loadPaymentMethodsForRow($(this));
        loadSubCategoriesForRow($(this));
    });
});
