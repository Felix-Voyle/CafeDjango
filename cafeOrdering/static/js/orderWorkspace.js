function setAddress() {
    var value = $('#selectWorkspace').find(":selected").val()
    var string = value.toString()
    var addressLine1 = $('#address_line1')
    var addressLine2 = $('#address_line2')
    var addressLine3 = $('#address_line3')
    var postcode = $('#postcode')
    workspaces = {
        "Cargo Works": {
            "address_line_1": "Cargo Works",
            "address_line_2": "1-2 Hatfields",
            "address_line_3": "London",
            "postcode": "SE1 9PG"
        },
        "Print Rooms": {
            "address_line_1": "Print Rooms",
            "address_line_2": "House 164 - 180 Union St",
            "address_line_3": "London",
            "postcode": "SE1 0GE"
        },
        "Edinburgh House": {
            "address_line_1": "Edinburgh House",
            "address_line_2": "170 Kennington Ln",
            "address_line_3": "London",
            "postcode": "SE11 5DP"
        },
        "ScreenWorks": {
            "address_line_1": "ScreenWorks",
            "address_line_2": "22 Highbury Grove",
            "address_line_3": "London",
            "postcode": "N5 2EF"
        },
        "Light Bulb": {
            "address_line_1": "The Light Bulb",
            "address_line_2": "1 Filament Walk",
            "address_line_3": "London",
            "postcode": "SW18 4GQ"
        },
        "Frames": {
            "address_line_1": "The Frames",
            "address_line_2": "1 Phipp St",
            "address_line_3": "London",
            "postcode": "EC2A 4PS"
        },
        "Barley Mow": {
            "address_line_1": "The Barley Mow Centre",
            "address_line_2": "10 Barley Mow Passage",
            "address_line_3": "Chiswick",
            "postcode": "W4 4PH"
        },
        "Vox Studios": {
            "address_line_1": "Vox Studios",
            "address_line_2": "1-45 Durham St",
            "address_line_3": "London",
            "postcode": "SE11 5JH"
        }
    }

    if (workspaces[string]) {
        addressLine1.val(workspaces[string].address_line_1);
        addressLine2.val(workspaces[string].address_line_2);
        addressLine3.val(workspaces[string].address_line_3);
        postcode.val(workspaces[string].postcode);
    }
}