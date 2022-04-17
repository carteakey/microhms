function populate() {

    let total = 0;
    let table = document.getElementById("data");
    let tbody = table.getElementsByTagName("tbody")[0];
    let rows = tbody.getElementsByTagName("tr");

    function populateRow(index) {
        let row = rows[index];
        let select = row.getElementsByTagName("select");
        let textboxes = row.getElementsByTagName("input");

        let charge = select[0];
        let hsn = textboxes[0];
        let sell_rate = textboxes[2];
        let inclusion = textboxes[3];
        let subtotal = textboxes[4];
        let cgst = textboxes[5];
        let sgst = textboxes[6];
        let line_total = textboxes[7];


        function updateHSN() {

            fetch("/get_hsn/" + charge.value).then(function (response) {
                return response.text();
            }).then(function (text) {
                console.log('get_hsn response:');
                console.log(text);
                hsn.value = parseFloat(text);

            });

        }

        function updateGST() {

            fetch("/get_gst/" + subtotal.value).then(function (response) {
                return response.text();
            }).then(function (text) {
                console.log('get_gst response:');
                console.log(text);
                cgst.value = parseFloat(text);
                sgst.value = parseFloat(text);

            });

        }

        function updateSubTotal() {
            sr = sell_rate.value.length > 0 ? parseFloat(sell_rate.value) : 0
            inc = inclusion.value.length > 0 ? parseFloat(inclusion.value) : 0
            subtotal.value = (sr + inc).toFixed(2);
        }

        function updateLineTotal() {
            sub = subtotal.value.length > 0 ? parseFloat(subtotal.value) : 0
            ct = cgst.value.length > 0 ? parseFloat(cgst.value) : 0
            st = sgst.value.length > 0 ? parseFloat(sgst.value) : 0
            line_total.value = (sub + ct + st).toFixed(2);
        }


        updateHSN();
        updateSubTotal();
        updateGST();
        updateLineTotal();

        total = parseFloat(total) + parseFloat(line_total.value)


    }

   
    for (i = 0; i < rows.length; i++) {
        populateRow(i);
    }

    let tpr = document.getElementById("tpr");
    console.log('Total:'+total)
    tpr.value = parseFloat(total).toFixed(2);;


};


window.onload = function () {
    let payee = document.getElementById("payee");
    let guest = document.getElementById("guest");

    payee.addEventListener('input', function () {
        guest.value = payee.value
    });

    populate();

};