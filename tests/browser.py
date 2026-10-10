"""Run against the locally served project: python tests/browser.py [base_url]."""
import asyncio,sys,json
from pathlib import Path
from playwright.async_api import async_playwright
async def main():
    base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8837'
    output=Path(__file__).resolve().parents[1]/'artifacts';output.mkdir(exist_ok=True)
    checks=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        page=await browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
        page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
        await page.goto(base,wait_until='networkidle')
        await page.locator('h1').wait_for()
        await page.screenshot(path=str(output/'clearvue-desktop.png'),full_page=True)
        await page.get_by_role('button',name='Dialog Overlay',exact=True).click()
        trigger=page.get_by_role('button',name='Open dialog')
        await trigger.click()
        dialog=page.get_by_role('dialog')
        assert await dialog.is_visible()
        assert await page.evaluate('document.activeElement.textContent')=='Close dialog'
        # Native modal Tab/Shift+Tab wrap stays within the modal.
        for key in ['Tab','Tab','Shift+Tab','Shift+Tab']:
            await page.keyboard.press(key)
            assert await page.evaluate('!!document.activeElement.closest("dialog")')
        await page.screenshot(path=str(output/'clearvue-dialog.png'))
        await page.keyboard.press('Escape')
        assert not await dialog.is_visible()
        assert await trigger.evaluate('(el)=>el===document.activeElement')
        checks.append('Dialog: initial focus, modal focus containment, Escape, trigger focus restoration')
        await page.get_by_role('button',name='Tabs Navigation',exact=True).click()
        tabs=page.get_by_role('tab')
        await tabs.nth(0).focus();await page.keyboard.press('ArrowRight')
        assert await tabs.nth(1).get_attribute('aria-selected')=='true'
        assert await tabs.nth(1).evaluate('(el)=>el===document.activeElement')
        await page.keyboard.press('End');assert await tabs.nth(2).get_attribute('aria-selected')=='true'
        await page.keyboard.press('ArrowRight');assert await tabs.nth(0).get_attribute('aria-selected')=='true'
        await page.keyboard.press('ArrowLeft');assert await tabs.nth(2).get_attribute('aria-selected')=='true'
        await page.keyboard.press('Home');assert await tabs.nth(0).get_attribute('aria-selected')=='true'
        checks.append('Tabs: arrows wrap, Home/End, selected state and roving focus')
        await page.get_by_role('button',name='Text input Input',exact=True).click()
        await page.get_by_role('button',name='Check email').click()
        email=page.get_by_role('textbox',name='Email address')
        assert await email.get_attribute('aria-invalid')=='true'
        assert 'demo-email-error' in await email.get_attribute('aria-describedby')
        assert await email.evaluate('(el)=>el===document.activeElement')
        await email.fill('review@example.com');await page.get_by_role('button',name='Check email').click()
        assert await email.get_attribute('aria-invalid') is None
        assert await page.get_by_role('status').inner_text()=='Email accepted for this demo. Nothing was sent.'
        checks.append('Input: label association, error relationship, invalid state, valid recovery and focus')
        await page.get_by_role('button',name='Disclosure Content',exact=True).click()
        disclosure=page.get_by_role('button',name='What makes this keyboard friendly?')
        await disclosure.focus();await page.keyboard.press('Enter')
        assert await disclosure.get_attribute('aria-expanded')=='true'
        await page.keyboard.press('Space');assert await disclosure.get_attribute('aria-expanded')=='false'
        checks.append('Disclosure: Enter/Space and expanded state')
        await page.get_by_role('button',name='Button Action',exact=True).click()
        save=page.get_by_role('button',name='Save changes',exact=True)
        await save.focus();await page.keyboard.press('Enter')
        assert 'Saved 1 time' in await page.get_by_role('status').inner_text()
        assert await page.get_by_role('button',name='Unavailable').is_disabled()
        checks.append('Button: keyboard activation and native disabled state')
        await page.get_by_role('button',name='Alert Feedback',exact=True).click()
        await page.get_by_role('button',name='Save preferences').click()
        assert 'Preferences saved' in await page.get_by_role('status').inner_text()
        checks.append('Alert: live status updates')
        await page.get_by_role('button',name='Dialog Overlay',exact=True).click()
        await page.get_by_role('button',name='Dark mode',exact=True).click()
        assert await page.locator('html').get_attribute('data-theme')=='dark'
        await page.reload(wait_until='networkidle')
        assert await page.locator('html').get_attribute('data-theme')=='dark'
        await page.screenshot(path=str(output/'clearvue-dark.png'),full_page=True)
        checks.append('Theme: toggle and local persistence')
        await page.get_by_role('button',name='Light mode',exact=True).click()
        await page.set_viewport_size({'width':390,'height':844})
        await page.screenshot(path=str(output/'clearvue-mobile.png'),full_page=True)
        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        checks.append('Mobile: 390px viewport without horizontal page overflow')
        assert not errors,errors
        checks.append('No browser runtime errors')
        (output/'checks.json').write_text(json.dumps({'base_url':base,'checks':checks,'errors':errors},indent=2))
        print(json.dumps({'passed':len(checks),'checks':checks},indent=2))
        await browser.close()
asyncio.run(main())
