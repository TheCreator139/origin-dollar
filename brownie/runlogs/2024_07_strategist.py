# -------------------------------------
# Jul 04, 2024 - OETH Buyback
# -------------------------------------
from buyback import *
def main():
  txs = []

  oeth_for_ogn, oeth_for_cvx = get_balance_splits(OETH)

  with TemporaryFork():
    txs.append(
      build_1inch_buyback_tx(
        OETH,
        OGN,
        oeth_for_ogn,
        3.5
      )
    )

    txs.append(
      build_1inch_buyback_tx(
        OETH,
        CVX,
        oeth_for_cvx,
        2
      )
    )

    txs.append(
      cvx_locker.processExpiredLocks(True, std)
    )

    print(to_gnosis_json(txs))

# -------------------------------------
# Jul 04, 2024 - OUSD Buyback
# -------------------------------------
from buyback import *
def main():
  txs = []

  ousd_for_ogn, ousd_for_cvx = get_balance_splits(OUSD)

  with TemporaryFork():
    txs.append(
      build_1inch_buyback_tx(
        OUSD,
        OGN,
        ousd_for_ogn,
        3
      )
    )

    txs.append(
      build_1inch_buyback_tx(
        OUSD,
        CVX,
        ousd_for_cvx,
        2
      )
    )

    print(to_gnosis_json(txs))


# -------------------------------------
# Jul 5, 2024 - Second deposit to Native Staking Strategy
# -------------------------------------
from world import *

def main():
  with TemporaryForkForReallocations() as txs:
    # Before
    txs.append(vault_oeth_core.rebase(std))
    txs.append(oeth_vault_value_checker.takeSnapshot(std))
    
    # Deposit WETH to Native Staking Strategy
    txs.append(
      vault_oeth_admin.depositToStrategy(
        OETH_NATIVE_STAKING_STRAT, 
        [WETH], 
        [740 * 10**18],
        std
      )
    )

    # After
    vault_change = vault_oeth_core.totalValue() - oeth_vault_value_checker.snapshots(STRATEGIST)[0]
    supply_change = oeth.totalSupply() - oeth_vault_value_checker.snapshots(STRATEGIST)[1]
    profit = vault_change - supply_change
    txs.append(oeth_vault_value_checker.checkDelta(profit, (1 * 10**18), vault_change, (1 * 10**18), std))
    print("-----")
    print("Profit", "{:.6f}".format(profit / 10**18), profit)
    print("OETH supply change", "{:.6f}".format(supply_change / 10**18), supply_change)
    print("Vault Change", "{:.6f}".format(vault_change / 10**18), vault_change)
    print("-----")
