{
  "version": "5.1",
  "screens": [
    {
      "id": "RECOMMEND",
      "title": "Profile Details",
      "data": {},
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "Form",
            "name": "flow_path",
            "children": [
              {
                "type": "TextSubheading",
                "text": "Enter your name"
              },
              {
                "type": "TextInput",
                "label": "name",
                "name": "TextInput_f2ad32",
                "required": true,
                "input-type": "text"
              },
              {
                "type": "TextSubheading",
                "text": "Enter your email"
              },
              {
                "type": "TextInput",
                "label": "example@gmail.com",
                "name": "TextInput_ef0d0e",
                "required": true,
                "input-type": "text"
              },
              {
                "type": "Footer",
                "label": "Submit",
                "on-click-action": {
                  "name": "navigate",
                  "next": {
                    "type": "screen",
                    "name": "screen_mxggbc"
                  },
                  "payload": {
                    "screen_0_TextInput_0": "${form.TextInput_f2ad32}",
                    "screen_0_TextInput_1": "${form.TextInput_ef0d0e}"
                  }
                }
              }
            ]
          }
        ]
      }
    },
    {
      "id": "screen_mxggbc",
      "title": "Event Details",
      "data": {
        "screen_0_TextInput_0": {
          "type": "string",
          "__example__": "Example"
        },
        "screen_0_TextInput_1": {
          "type": "string",
          "__example__": "Example"
        }
      },
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "Form",
            "name": "flow_path",
            "children": [
              {
                "type": "TextSubheading",
                "text": "Select the events to attend"
              },
              {
                "type": "CheckboxGroup",
                "label": "Event Name:(Max. Participants)",
                "required": true,
                "name": "CheckboxGroup_14ca70",
                "data-source": [
                  {
                    "id": "0_Battle_of_Bands:_(6)",
                    "title": "Battle of Bands: (6)"
                  },
                  {
                    "id": "1_Blind_Date:_(1)",
                    "title": "Blind Date: (1)"
                  },
                  {
                    "id": "2_Treasure_Hunt:_(2)",
                    "title": "Treasure Hunt: (2)"
                  },
                  {
                    "id": "3_Mystery_Room:_(4)",
                    "title": "Mystery Room: (4)"
                  },
                  {
                    "id": "4_Drama_Wars:_(6)",
                    "title": "Drama Wars: (6)"
                  },
                  {
                    "id": "5_Dance_Battle:_(4)",
                    "title": "Dance Battle: (4)"
                  },
                  {
                    "id": "6_Gokarting:_(1)",
                    "title": "Gokarting: (1)"
                  },
                  {
                    "id": "7_Panipuri:_(1)",
                    "title": "Panipuri: (1)"
                  },
                  {
                    "id": "8_Human_Foose_Ball:_(1)",
                    "title": "Human Foose Ball: (1)"
                  }
                ]
              },
              {
                "type": "Footer",
                "label": "Submit",
                "on-click-action": {
                  "name": "navigate",
                  "next": {
                    "type": "screen",
                    "name": "screen_fsvykg"
                  },
                  "payload": {
                    "screen_1_CheckboxGroup_0": "${form.CheckboxGroup_14ca70}",
                    "screen_0_TextInput_0": "${data.screen_0_TextInput_0}",
                    "screen_0_TextInput_1": "${data.screen_0_TextInput_1}"
                  }
                }
              }
            ]
          }
        ]
      }
    },
    {
      "id": "screen_fsvykg",
      "title": "Additional Info 1",
      "data": {
        "screen_1_CheckboxGroup_0": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "__example__": []
        },
        "screen_0_TextInput_0": {
          "type": "string",
          "__example__": "Example"
        },
        "screen_0_TextInput_1": {
          "type": "string",
          "__example__": "Example"
        }
      },
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "Form",
            "name": "flow_path",
            "children": [
              {
                "type": "TextSubheading",
                "text": "No. of people participating in Battle of Bands"
              },
              {
                "type": "Dropdown",
                "label": "Upto 6",
                "required": true,
                "name": "Dropdown_bedd2a",
                "data-source": [
                  {
                    "id": "0_1",
                    "title": "1"
                  },
                  {
                    "id": "1_2",
                    "title": "2"
                  },
                  {
                    "id": "2_3",
                    "title": "3"
                  },
                  {
                    "id": "3_4",
                    "title": "4"
                  },
                  {
                    "id": "4_5",
                    "title": "5"
                  },
                  {
                    "id": "5_6",
                    "title": "6"
                  }
                ]
              },
              {
                "type": "Footer",
                "label": "Continue",
                "on-click-action": {
                  "name": "navigate",
                  "next": {
                    "type": "screen",
                    "name": "screen_hvkcqr"
                  },
                  "payload": {
                    "screen_2_Dropdown_0": "${form.Dropdown_bedd2a}",
                    "screen_1_CheckboxGroup_0": "${data.screen_1_CheckboxGroup_0}",
                    "screen_0_TextInput_0": "${data.screen_0_TextInput_0}",
                    "screen_0_TextInput_1": "${data.screen_0_TextInput_1}"
                  }
                }
              }
            ]
          }
        ]
      }
    },
    {
      "id": "screen_hvkcqr",
      "title": "Additional Info 2",
      "data": {
        "screen_2_Dropdown_0": {
          "type": "string",
          "__example__": "Example"
        },
        "screen_1_CheckboxGroup_0": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "__example__": []
        },
        "screen_0_TextInput_0": {
          "type": "string",
          "__example__": "Example"
        },
        "screen_0_TextInput_1": {
          "type": "string",
          "__example__": "Example"
        }
      },
      "terminal": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "Form",
            "name": "flow_path",
            "children": [
              {
                "type": "TextSubheading",
                "text": "No. of people participating in Treasure Hunt"
              },
              {
                "type": "Dropdown",
                "label": "Upto 2",
                "required": true,
                "name": "Dropdown_854df3",
                "data-source": [
                  {
                    "id": "0_1",
                    "title": "1"
                  },
                  {
                    "id": "1_2",
                    "title": "2"
                  }
                ]
              },
              {
                "type": "Footer",
                "label": "Submit",
                "on-click-action": {
                  "name": "complete",
                  "payload": {
                    "screen_3_Dropdown_0": "${form.Dropdown_854df3}",
                    "screen_2_Dropdown_0": "${data.screen_2_Dropdown_0}",
                    "screen_1_CheckboxGroup_0": "${data.screen_1_CheckboxGroup_0}",
                    "screen_0_TextInput_0": "${data.screen_0_TextInput_0}",
                    "screen_0_TextInput_1": "${data.screen_0_TextInput_1}"
                  }
                }
              }
            ]
          }
        ]
      }
    }
  ]
}