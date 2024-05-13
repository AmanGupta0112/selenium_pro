from django.shortcuts import render, redirect
from django.http import HttpResponse
from .constants import DATES, OPTIONS, SEARCH_ARROW, STATES, BANKS
from .selenium_scrap import get_driver, find_ele_xpath, find_ele_tag, find_ele_id, download
import time

def home(request):
    return HttpResponse("Welcome to cibil scraper!")

def dropdown_form_view(request):
    dates = DATES
    options = OPTIONS.keys()
    if request.method == "POST":
        request_body = request.POST
        if "quarterIdSummary" in request_body:
            try:
                get_summary_view(request_body.get("quarterIdSummary"), "quarterIdSummary")
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")
        elif "quarterIdGrantors" in request_body:
            try:
                get_summary_view(request_body.get("quarterIdGrantors"), "quarterIdGrantors")
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")
        else:
            return HttpResponse("Invalid request")
    return render(request, "cibil_scrap/suit_cibil_home.html", context={"dates": dates, "options": options})

def get_summary_view(*args):
    try:
        driver = get_driver()
        ele = find_ele_id(driver, args[1])
        idx = DATES.index(args[0])
        find_ele_tag(ele, 'option', idx+1)
        if args[1] == "quarterIdSummary":
            find_ele_xpath(driver, SEARCH_ARROW[0])
        else:
            find_ele_xpath(driver, SEARCH_ARROW[1])
        time.sleep(2)
        download(driver)
        time.sleep(2)
    except Exception as e:
        raise e
    finally:
        driver.quit()

def get_account_view(*args):
    try:
        driver = get_driver()
        ele = find_ele_id(driver, args[1])
        op, date = args[0][0], args[0][1]
        op_id = OPTIONS.get(op)
        find_ele_tag(ele, "option", op_id)
        time.sleep(2)
        ele2 = find_ele_id(driver, args[2])
        idx = DATES.index(date)
        find_ele_tag(ele2, "option", idx)
        if args[2] == "quarterIdCrore":
            find_ele_xpath(driver, SEARCH_ARROW[2])
        else:
            find_ele_xpath(driver, SEARCH_ARROW[3])
        time.sleep(2)
        if "Search" not in args[0]:
            download(driver)
            time.sleep(2)
    except Exception as e:
        raise e
    finally:
        driver.quit()
    return driver

def suit_cibil_search(request):
    try:
        request_body = request.POST
        request_list = request_body.getlist("request_list")
        if "croreAccount" in request_list:
            driver = get_account_view(request_list, "croreAccount", "quarterIdCrore")
        else:
            driver = get_account_view(request_list, "lakhAccount", "quarterIdLakh")

        borrow = find_ele_id(driver, "borrowerName")
        borrow.send_keys(request_body.get("borrower_name", ""))
        director = find_ele_id(driver, "directorName")
        director.send_keys(request_body.get("director_name", ""))
        din = find_ele_id(driver, "directorDin")
        din.send_keys(request_body.get("director_din", ""))
        bank = find_ele_id(driver, "bankId")
        bank_id = BANKS.index(request_body.get("institutions", "ALL"))
        find_ele_tag(bank, "option", bank_id)
        state = find_ele_id(driver, "stateId")
        state_id = STATES.index(request_body.get("state_union", ""))
        find_ele_tag(state, "option", state_id)
        city = find_ele_id(driver, "city")
        city.send_keys(request_body.get("city", ""))
        find_ele_xpath(driver, '//*[@id="search-button"]/ul/li[1]/div/input')
        time.sleep(15)
        download(driver)
        time.sleep(2)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    finally:
        driver.quit()
    return HttpResponse("OK")

def cibil_search(request):
    if request.method == "POST":
        try:
            request_body = request.POST
            request_list = []
            if "croreAccount" in request_body:
                request_list = request_body.getlist("croreAccount")
                if "Search" in request_list:
                    print("request_list:", request_list)
                    request_list.append("croreAccount")
                    return render(
                        request,
                        "cibil_scrap/suit_cibil_search.html",
                        {
                            "request_list": request_list,
                            "states": STATES[1:],
                            "credits": BANKS[1:],
                        },
                    )
                driver = get_account_view(request_list, "croreAccount", "quarterIdCrore")
            elif "lakhAccount" in request_body:
                request_list = request_body.getlist("lakhAccount")
                if "Search" in request_list[0]:
                    request_list.append("lakhAccount")
                    return render(
                        request,
                        "cibil_scrap/suit_cibil_search.html",
                        {
                            "request_list": request_list,
                            "states": STATES[1:],
                            "credits": BANKS[1:],
                        },
                    )
                driver = get_account_view(request_list, "lakhAccount", "quarterIdLakh")
            else:
                return HttpResponse("Invalid request")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    return HttpResponse("OK")
